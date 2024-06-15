#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of nannos
# License: GPLv3
# See the documentation at nannos.gitlab.io


import numpy as npo
from scipy.optimize import minimize

from . import DEVICE
from . import backend as bk
from . import get_backend, get_types, grad
from .log import logger
from .utils import apply_filter, tic, toc

FLOAT, COMPLEX = get_types()


def simp(x, eps_min, eps_max, p=1):
    return (eps_max - eps_min) * x**p + eps_min


def project(x, beta=1, thres=0.5):
    x = bk.array(x)

    def tanh(z):
        return bk.tanh(bk.array(z))

    return ((tanh(thres * beta)) + tanh(beta * (x - thres))) / (
        tanh(thres * beta) + (tanh((1 - thres) * beta))
    )


def multi_project(x, beta=1, Nthres=2):
    thresholds = bk.linspace(0, 1, Nthres + 1)[1:-1]
    out = sum(project(x, beta, thres) for thres in thresholds)
    return out / len(thresholds)


def multi_simp(x, epsilons, p=1):
    epsilons = bk.array(epsilons) + 0j
    nthres = len(epsilons)
    npts = nthres
    if nthres == 2:
        return simp(x, epsilons[0], epsilons[1], p)
    pts = bk.linspace(0, 1, npts)

    def pol(coefs, x):
        return sum(c * x ** (n * p) for n, c in enumerate(coefs))

    def mat(pts):
        return bk.array([[_x ** (n * p) + 0j for n in range(npts)] for _x in pts])

    M = mat(pts)
    coefs = bk.linalg.inv(M) @ epsilons
    return pol(coefs, x)


class StopFunError(Exception):
    """Raised when stop value reached"""

    pass


class StopFun:
    def __init__(self, fun, stopval=None):
        self.fun_in = fun
        self.stopval = stopval

    def fun(self, x, *args):
        self.f = self.fun_in(x, *args)
        if self.stopval is not None and self.f < self.stopval:
            raise StopFunError("Stop value reached.")
        self.x = x
        return self.f


class TopologyOptimizer:
    def __init__(
        self,
        fun,
        x0,
        method="scipy",
        threshold=(0, 8),
        maxiter=10,
        stopval=None,
        args=None,
        callback=None,
        verbose=False,
        options=None,
    ):
        if method == "nlopt":
            try:
                import nlopt

                self.nlopt = nlopt
            except:
                logger.info("nlopt not installed, falling back to scipy.optimize")
                method = "scipy"
        if options is None:
            options = {}
        self.fun = fun
        self.x0 = x0
        self.nvar = len(x0)
        self.method = method
        self.threshold = threshold
        self.maxiter = maxiter
        self.stopval = stopval
        self.args = args
        self.callback = callback
        self.verbose = verbose
        self.options = options
        self.grad_fun = grad(fun)

        self.current_iteration = 0

    def print(self, s):
        if self.verbose:
            return print(s)

    def minimize(self):
        self.print("#################################################")
        self.print(f"Topology optimization with {self.nvar} variables")
        self.print("#################################################")
        self.print("")
        x0 = (
            self.x0.cpu()
            if (get_backend() == "torch" and DEVICE == "cuda")
            else self.x0
        )
        x0 = npo.array(x0)
        for iopt in range(*self.threshold):
            self.print("-----------------------")
            self.print(f"  global iteration {iopt}")
            self.print("-----------------------")

            proj_level = 2**iopt
            args = list(self.args)
            args[0] = proj_level
            args = tuple(args)
            if self.method == "scipy":

                def fun_scipy(x, *args):
                    self.print(f">>> iteration {self.current_iteration}")
                    x = bk.array(x, dtype=FLOAT)
                    y = self.fun(x, *args)
                    self.print(f"current value = {y}")
                    if self.callback is not None:
                        self.callback(x, y, *args)
                    self.current_iteration += 1
                    return y

                bounds = [(0, 1) for _ in range(self.nvar)]
                options = {"maxiter": self.maxiter}
                if self.options is not None:
                    options.update(self.options)

                stop = StopFun(fun=fun_scipy, stopval=self.stopval)
                try:
                    self.opt = minimize(
                        stop.fun,
                        x0,
                        args=args,
                        method="L-BFGS-B",
                        jac=self.grad_fun,
                        bounds=bounds,
                        options=options,
                    )
                    xopt = self.opt.x
                    fopt = self.opt.fun
                except StopFunError as e:
                    print(e)
                    xopt = stop.x
                    fopt = stop.f

            else:

                def fun_nlopt(x, gradn):
                    self.print(f">>> iteration {self.current_iteration}")
                    x = bk.array(x, dtype=FLOAT)
                    y = self.fun(x, *args)
                    self.print(f"current value = {y}")
                    if self.callback is not None:
                        self.callback(x, y, *args)
                    if gradn.size > 0:
                        dy = self.grad_fun(x, *args)
                        dy = (
                            dy.cpu()
                            if (get_backend() == "torch" and DEVICE == "cuda")
                            else dy
                        )
                        gradn[:] = npo.array(dy, dtype=npo.float64)

                    self.current_iteration += 1
                    return float(y)

                lb = npo.zeros(self.nvar, dtype=npo.float64)
                ub = npo.ones(self.nvar, dtype=npo.float64)

                self.opt = self.nlopt.opt(self.nlopt.LD_MMA, self.nvar)
                self.opt.set_lower_bounds(lb)
                self.opt.set_upper_bounds(ub)
                if "ftol_rel" in self.options:
                    self.opt.set_ftol_rel(self.options["ftol_rel"])
                if "xtol_rel" in self.options:
                    self.opt.set_xtol_rel(self.options["xtol_rel"])
                if "ftol_abs" in self.options:
                    self.opt.set_ftol_abs(self.options["ftol_abs"])
                if "xtol_abs" in self.options:
                    self.opt.set_xtol_abs(self.options["xtol_abs"])
                if self.stopval is not None:
                    self.opt.set_stopval(self.stopval)
                if self.maxiter is not None:
                    self.opt.set_maxeval(self.maxiter)
                for k, v in self.options.items():
                    self.opt.set_param(k, v)
                self.opt.set_min_objective(fun_nlopt)
                xopt = self.opt.optimize(x0)
                fopt = self.opt.last_optimum_value()
            x0 = xopt
        return xopt, fopt
