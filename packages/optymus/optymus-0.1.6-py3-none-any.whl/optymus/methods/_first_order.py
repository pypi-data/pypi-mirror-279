import time

import jax
import jax.numpy as jnp
from tqdm import tqdm

from optymus.search import line_search


def gradient_descent(f_obj=None, f_cons=None, args=(), args_cons=(), x0=None, tol=1e-4, learning_rate=0.01, max_iter=100, verbose=True, maximize=False):
    r"""Gradient Descent

    Gradient Descent is a first-order optimization algorithm that uses the
    gradient of the objective function to compute the step direction.

    We can minimize the objective function :math:`f` by solving the following
    equation:

    .. math::
        x_{k+1} = x_k - \alpha \nabla f(x_k)

    where :math:`x_k` is the current point, :math:`\alpha` is the step size,
    and :math:`\nabla f(x_k)` is the gradient of :math:`f` evaluated at point
    :math:`x_k`.

    Parameters
    ----------
    f_obj : callable
        Objective function to minimize
    f_cons : callable
        Constraint function
    args : tuple
        Arguments for the objective function
    args_cons : tuple
        Arguments for the constraint function
    x0 : ndarray
        Initial guess
    tol : float
        Tolerance for stopping criteria
    learning_rate : float
        Step size
    max_iter : int
        Maximum number of iterations
    maximize : bool
        If True, maximize the objective function

    Returns
    -------
    method_name : str
        Method name
    xopt : ndarray
        Optimal point
    fmin : float
        Minimum value
    num_iter : int
        Number of iterations
    path : ndarray
        Path taken
    alphas : ndarray
        Step sizes
    """
    start_time = time.time()
    x = x0.astype(float)  # Ensure x0 is of a floating-point type

    def penalized_obj(x):
        penalty = 0.0
        if f_cons is not None:
            for f_con in f_cons:
                penalty += jnp.sum(jnp.maximum(0, f_con(x, *args_cons)) ** 2)
        if maximize:
            return -f_obj(x, *args) + penalty
        return f_obj(x, *args) + penalty

    grad = jax.grad(penalized_obj)(x)
    d = grad
    path = [x]
    alphas = []
    num_iter = 0

    progres_bar = tqdm(range(max_iter), desc=f'Gradient Descent {num_iter}',) if verbose else range(max_iter)

    for _ in progres_bar:
        if jnp.linalg.norm(grad) < tol:
            break
        r = line_search(f=penalized_obj, x=x, d=d, learning_rate=learning_rate)
        x = r['xopt'].astype(float)  # Ensure xopt is of a floating-point type
        grad = jax.grad(penalized_obj)(x)
        d = grad
        path.append(x)
        alphas.append(r['alpha'])
        num_iter += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    return {
        'method_name': 'Gradient Descent' if not f_cons else 'Gradient Descent with Penalty',
        'x0':x0,
        'xopt': x,
        'fmin': f_obj(x, *args),
        'num_iter': num_iter,
        'path': jnp.array(path),
        'alphas': jnp.array(alphas),
        'time': elapsed_time
    }


def conjugate_gradient(f_obj=None, f_cons=None, args=(), args_cons=(), x0=None, tol=1e-5, learning_rate=0.01, max_iter=100, verbose=True, gradient_type='fletcher_reeves', maximize=False):
    r"""Conjugate Gradient

    Conjugate Gradient is a first-order optimization algorithm that uses the
    gradient of the objective function to compute the step direction.

    We can minimize the objective function :math:`f` by solving the following
    equation:

    .. math::
        x_{k+1} = x_k - \alpha_k d_k

    where :math:`x_k` is the current point, :math:`\alpha_k` is the step size,
    and :math:`d_k` is the search direction.

    The search direction :math:`d_k` is computed as follows:

    .. math::
        d_k = -\nabla f(x_k) + \beta_k d_{k-1}

    where :math:`\nabla f(x_k)` is the gradient of :math:`f` evaluated at point
    :math:`x_k`, and :math:`\beta_k` is the conjugate gradient coefficient.

    We can compute beta using different formulas:

    - Fletcher-Reeves: :math:`\beta_k = \frac{\nabla x_k^{T} \nabla x_k}{\nabla x_{k-1}^{T} \nabla x_{k-1}}`
    - Polak-Ribiere: :math:`\beta_k = \frac{\nabla x_k^{T} (\nabla x_k - \nabla x_{k-1})}{\nabla x_{k-1}^T \nabla x_{k-1}}`
    - Hestnes-Stiefel: :math:`\beta_k = \frac{\nabla x_k^{T} (\nabla x_k - \nabla x_{k-1})}{\nabla s_{k-1}^{T}(\nabla x_{k} - \nabla x_{k-1})}` 
    - Dai-Yuan: :math:`\beta_k = \frac{\nabla x_{k}^{T} \nabla x_{k}}{\nabla s_{k-1}^{T}(\nabla x_{k} - \nabla x_{k-1})}`

    Parameters
    ----------
    f_obj : callable
        Objective function to minimize
    f_cons : callable
        Constraint function
    args : tuple
        Arguments for the objective function
    args_cons : tuple
        Arguments for the constraint function
    x0 : ndarray
        Initial guess
    tol : float
        Tolerance for stopping criteria
    learning_rate : float
        Step size
    max_iter : int
        Maximum number of iterations
    gradien_type: str
        'fletcher_reeves', 'polak_ribiere', 'hestnes_stiefel', 'dai_yuan'
    maximize : bool
        If True, maximize the objective function

    Returns
    -------
    method_name : str
        Method name
    xopt : ndarray
        Optimal point
    fmin : float
        Minimum value
    num_iter : int
        Number of iterations
    path : ndarray
        Path taken
    alphas : ndarray
        Step sizes
    """  # noqa: E501
    start_time = time.time()
    x = x0.astype(float)  # Ensure x0 is of a floating-point type

    def penalized_obj(x):
        penalty = 0.0
        if f_cons is not None:
            for f_con in f_cons:
                penalty += jnp.sum(jnp.maximum(0, f_con(x, *args_cons)) ** 2)
        if maximize:
            return -f_obj(x, *args) + penalty
        return f_obj(x, *args) + penalty

    grad = jax.grad(penalized_obj)(x)
    d = grad
    path = [x]
    alphas = []
    num_iter = 0

    progres_bar = tqdm(range(max_iter), desc=f'Conjugate Gradient {num_iter}',) if verbose else range(max_iter)

    for _ in progres_bar:
        if jnp.linalg.norm(grad) <= tol:
            break
        r = line_search(f=penalized_obj, x=x, d=d, learning_rate=learning_rate)
        x = r['xopt']
        new_grad = jax.grad(penalized_obj)(x)
        if jnp.linalg.norm(new_grad) <= tol:
            break

        if gradient_type == 'fletcher_reeves':
            beta = jnp.dot(new_grad, new_grad) / jnp.dot(grad, grad)

        elif gradient_type == 'polak_ribiere':
            beta = jnp.dot(new_grad, new_grad - grad) / jnp.dot(grad, grad)

        elif gradient_type == 'hestnes_stiefel':
            beta = jnp.dot(new_grad, new_grad-grad) / jnp.dot(d, new_grad-grad)

        elif gradient_type == 'dai_yuan':
            beta = jnp.dot(new_grad, new_grad) / jnp.dot(d, new_grad-grad)

        d = new_grad + beta * d
        r = line_search(f=penalized_obj, x=x, d=d, learning_rate=learning_rate)
        x = r['xopt']
        alphas.append(r['alpha'])
        path.append(x)
        num_iter += 1
    end_time = time.time()
    elapsed_time = end_time - start_time

    return {
        'method_name': f'Conjugate Gradients ({gradient_type})' if not f_cons else f'Conjugate Gradients ({gradient_type}) with Penalty',
        'x0':x0,
        'xopt': x,
        'fmin': f_obj(x, *args),
        'num_iter': num_iter,
        'path': jnp.array(path),
        'alphas': jnp.array(alphas),
        'time':elapsed_time
        }


def bfgs(f_obj=None, f_cons=None, args=(), args_cons=(), x0=None, tol=1e-5, learning_rate=0.01, max_iter=100, verbose=True, maximize=False):
    r"""BFGS

    BFGS is a first-order optimization algorithm that uses the gradient of the
    objective function to compute the step direction.

    We can minimize the objective function :math:`f` by solving the following
    equation:

    .. math::
        x_{k+1} = x_k - \alpha_k d_k

    where :math:`x_k` is the current point, :math:`\alpha_k` is the step size,
    and :math:`d_k` is the search direction.

    The search direction :math:`d_k` is computed as follows:

    .. math::
        d_k = -B_k^{-1} \nabla f(x_k)

    where :math:`B_k` is an approximation of the inverse Hessian matrix.

    The inverse Hessian matrix :math:`B_k` is updated using the BFGS formula:

    .. math::
        B_{k+1} = B_k - \frac{B_k s_k s_k^T B_k}{s_k^T B_k s_k} + \frac{\delta_k \delta_k^T}{s_k^T \delta_k}

    where :math:`s_k = x_{k+1} - x_k`, :math:`\delta_k = \nabla f(x_{k+1}) - \nabla f(x_k)`.
    The step size :math:`\alpha_k` is computed using a line search algorithm.

    Parameters
    ----------
    f_obj : callable
        Objective function to minimize
    f_cons : callable
        Constraint function
    args : tuple
        Arguments for the objective function
    args_cons : tuple
        Arguments for the constraint function
    x0 : ndarray
        Initial guess
    tol : float
        Tolerance for stopping criteria
    learning_rate : float
        Step size
    max_iter : int
        Maximum number of iterations
    maximize : bool
        If True, maximize the objective function

    Returns
    -------
    method_name : str
        Method name
    xopt : ndarray
        Optimal point
    fmin : float
        Minimum value
    num_iter : int
        Number of iterations
    path : ndarray
        Path taken
    alphas : ndarray
        Step sizes
    """
    start_time = time.time()
    x = x0.astype(float)  # Ensure x0 is of a floating-point type

    def penalized_obj(x):
        penalty = 0.0
        if f_cons is not None:
            for f_con in f_cons:
                penalty += jnp.sum(jnp.maximum(0, f_con(x, *args_cons)) ** 2)
        if maximize:
            return -f_obj(x, *args) + penalty
        return f_obj(x, *args) + penalty

    path = [x]
    alphas = []
    num_iter = 0
    q = jnp.identity(len(x))  # Initial approximation of the inverse Hessian

    progres_bar = tqdm(range(max_iter), desc=f'BFGS {num_iter}',) if verbose else range(max_iter)

    for _ in progres_bar:
        grad = jax.grad(penalized_obj)(x)
        d = jnp.dot(q, grad)
        r = line_search(f=penalized_obj, x=x, d=d, learning_rate=learning_rate)
        x_new = r['xopt']
        delta = x_new - x
        gamma = jax.grad(penalized_obj)(x_new) - grad

        if jnp.linalg.norm(delta) < tol:
            break

        rho = 1.0 / jnp.dot(delta, gamma)
        q = (jnp.eye(len(x)) - rho * jnp.outer(delta, gamma)) @ q
        q = q @ (jnp.eye(len(x)) - rho * jnp.outer(gamma, delta))
        q = q + rho * jnp.outer(delta, delta)  # BFGS update

        x = x_new
        path.append(x)
        alphas.append(r['alpha'])
        num_iter += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    return {
        'method_name': 'BFGS' if not f_cons else 'BFGS with Penalty',
        'x0':x0,
        'xopt': x,
        'fmin': f_obj(x, *args),
        'num_iter': num_iter,
        'path': jnp.array(path),
        'alphas': jnp.array(alphas),
        'time':elapsed_time
    }

