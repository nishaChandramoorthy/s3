from numpy import *
import sys
dt = 0.01
def step(u, s=[10.,28.,8./3], n=1):
    '''
    Inputs:
        u: array of initial conditions, shape:mxd
        s: parameter array, shape:4
        n: number of timesteps
        m: number of initial conditions
    Output:
        primal trajectory, shape: (n+1)xdxm
    '''
    m = u.shape[0]
    d = u.shape[1]
    u_trj = empty((n+1,d,m))
    u_trj[0] = u.T
    sigma, rho, beta = s
    for i in range(n):
        x = u_trj[i,0]
        y = u_trj[i,1]
        z = u_trj[i,2]

        dxdt = sigma*(y - x)
        dydt = x*(rho - z) - y
        dzdt = x*y - beta*z

        u_trj[i+1,0] = x + dt*dxdt
        u_trj[i+1,1] = y + dt*dydt
        u_trj[i+1,2] = z + dt*dzdt

    return u_trj

def step2(u, s=[10.,28.,8./3], n=1):
    '''
    Inputs:
        u: array of initial conditions, shape:mxd
        s: parameter array, shape:4
        n: number of timesteps
        m: number of initial conditions
    Output:
        primal trajectory, shape: (n+1)xdxm
    '''
    m = u.shape[0]
    d = u.shape[1]
    u_trj = empty((n+1,d,m))
    u_trj[0] = u.T
    sigma, rho, beta = s
    for i in range(n):
        x = u_trj[i,0]
        y = u_trj[i,1]
        z = u_trj[i,2]

        dxdt = sigma*(y - x)
        dydt = x*(rho - z) - y
        dzdt = x*y - beta*z

        x1 = x + dt/2*dxdt
        y1 = y + dt/2*dydt
        z1 = z + dt/2*dzdt

        dxdt = sigma*(y1 - x1)
        dydt = x1*(rho - z1) - y1
        dzdt = x1*y1 - beta*z1


        u_trj[i+1,0] = x + dt*dxdt
        u_trj[i+1,1] = y + dt*dydt
        u_trj[i+1,2] = z + dt*dzdt

    return u_trj
def dstep(u, s=[10.,28.,8./3.]):
    """
    Input info:
    s: parameters, shape:4
    m: number of initial conditions
    u.shape = (m, d)
    
    Output:
    Jacobian matrices at each u
    shape: mxdxd
    """
    m, d = u.shape
    x, y, z = u.T

    sigma, rho, beta = s
    dTx_dx = (1.0 - dt*sigma)*ones(m)  
    dTx_dy = dt*sigma*ones(m)
    dTx_dz = zeros(m)
    dTy_dx = dt*(rho - z)*ones(m)
    dTy_dy = (1.0 - dt)*ones(m)
    dTy_dz = dt*(-x)
    dTz_dx = dt*y
    dTz_dy = dt*x
    dTz_dz = (1.0 - dt*beta)*ones(m)

    dTu_u = vstack([dTx_dx, dTx_dy, dTx_dz, \
                    dTy_dx, dTy_dy, dTy_dz, \
                    dTz_dx, dTz_dy, dTz_dz])
    dTu_u = dTu_u.T.reshape([-1,d,d])
    return dTu_u

def d2step(u, s):
    """
    This function computes D^2 varphi
    at the points u
    ddu[n,k,i,j] = d_k d_j u[n,i] 
    where u[n,i] is the ith component 
    of u_n.
    """
    n, d = u.shape
    ddu = zeros((n,d,d,d))
    ddu[:, 2, 1, 0] = -dt
    ddu[:, 0, 1, 2] = -dt
    ddu[:, 1, 2, 0] = dt
    ddu[:, 0, 2, 1] = dt
    return ddu

