from mssm.models import *
from mssm.src.python.custom_types import DerivOrder
import rpy2.rinterface as rinterface
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

class Tweedie(GAMLSSFamily):
    """Tweedie Family with variance function :math:`var(y_i)=\\phi_i\\mu_i^{p_i}`
    where :math:`\\mu_i`` is the mean of random variable :math:`y_i`.

    All three parameters can vary as smooth functions of covariates.

    The implementation here calls the ``ldTweedie`` function implemented in ``mgcv``
    in ``R``. Thus, this code cannot be parallelized and requires an installation of ``R``
    and ``rpy2``.

    References:
     - Wood, Pya, & Säfken (2016). Smoothing Parameter and Model Selection for General Smooth \
        Models.
     - Wood, S. N., & Fasiolo, M. (2017). A generalized Fellner-Schall method for smoothing \
        parameter optimization with application to Tweedie location, scale and shape models.
     - ``ldTweedie`` function in ``mgcv``, see: https://github.com/cran/mgcv/blob/master/R/gam.fit3.r#L2838

    :param link_mu: Link function to use for the mean.
    :type link_mu: Link
    :param a: Lower limit for ``p`` parameter. Should not be set below 1.01.
    :type a: float, optional
    :param b: Upper limit for ``p`` parameter. Should not be set above 1.99.
    :type b: float, optional
    :ivar float a: Value passed for ``a``.
    :ivar float b: Value passed for ``b``.
    """

    def __init__(self, link_mu=LOG(),a:float=1.01,b:float=1.99):
        super().__init__(3, [link_mu,Identity(),Identity()])
        self.__mgcv = importr("mgcv") # Hook to mgcv
        self.a = a
        self.b = b
    
    def dpars(self, y, *mus, index, order):
        """Returns partial derivatives of the log-likelihood with respect to the mean, ``p``, and
        ``rho`` or a combination indexed by ``index`` of ``order`` (first order, pure second,
        mixed second).

        All derivatives are computed by ``mgcv``'s ``ldTweedie`` function.

        References:
         - Wood, Pya, & Säfken (2016). Smoothing Parameter and Model Selection for General Smooth \
            Models.
         - Wood, S. N., & Fasiolo, M. (2017). A generalized Fellner-Schall method for smoothing \
            parameter optimization with application to Tweedie location, scale and shape models.
         - ``ldTweedie`` function in ``mgcv``, see: https://github.com/cran/mgcv/blob/master/R/gam.fit3.r#L2838

        :param y: A numpy array of shape (-1,1) containing each observed value.
        :type y: np.ndarray
        :param mus: 3 np arrays - for the mea, p, and rho parameters for the
            response distribution corresponding to each of N observations. Each numpy array is of
            shape (N,1).
        :type mus: np.ndarray
        :param index: Index for specific derivative vector to return.
        :type index: int
        :param order: Order of partial derivative.
        :type order: DerivOrder
        :return: a N-dimensional vector of shape (-1,1) containing the desired derivative evaluated
            for every observation in ``y``.
        :rtype: np.ndarray
        """
        mu = robjects.FloatVector(mus[0].flatten().tolist())
        theta = robjects.FloatVector(mus[1].flatten().tolist())
        rho = robjects.FloatVector(mus[2].flatten().tolist())
        
        ld = self.__mgcv.ldTweedie(robjects.FloatVector(y.flatten().tolist()),
                                   mu=mu,phi=rinterface.NA,
                                   rho=rho,theta=theta,
                                   a=self.a,b=self.b,
                                   **{'all.derivs': True})
        
        ld = np.array(ld)

        if order == DerivOrder.d1:
            if index == 0:
                dy1 = ld[:,[6]]
                return dy1
            elif index == 1:
                dy1 = ld[:,[3]]
                return dy1
            if index == 2:
                dy1 = ld[:,[1]]
                return dy1
            else:
                raise ValueError(f"No derivative of order d1 exists for index {index}")

        elif order == DerivOrder.d2:
            if index == 0:
                dy2 = ld[:,[7]]
                return dy2
            elif index == 1:
                dy2 = ld[:,[4]]
                return dy2
            elif index == 2:
                dy2 = ld[:,[2]]
                return dy2
            else:
                raise ValueError(f"No derivative of order d2 exists for index {index}")

        elif order == DerivOrder.d2m:
            if index == 0:
                # mt
                dy2m = ld[:,[8]]
                return dy2m
            elif index == 1:
                # mr
                dy2m = ld[:,[9]]
                return dy2m
            elif index == 2:
                # tr
                dy2m = ld[:,[5]]
                return dy2m
            else:
                raise ValueError(f"No derivative of order d2m exists for index {index}")

        raise ValueError("No Derivative > order d2m exists.")
    
    def lp(self, y, *mus):
        """Log-probability of observing every value in y under their respective Tweedie.

        All probabilities are computed by ``mgcv``'s ``ldTweedie`` function.

        References:
         - Wood, Pya, & Säfken (2016). Smoothing Parameter and Model Selection for General Smooth \
            Models.
         - Wood, S. N., & Fasiolo, M. (2017). A generalized Fellner-Schall method for smoothing \
            parameter optimization with application to Tweedie location, scale and shape models.
         - ``ldTweedie`` function in ``mgcv``, see: https://github.com/cran/mgcv/blob/master/R/gam.fit3.r#L2838

        :param y: A numpy array containing each observed value.
        :type y: np.ndarray
        :param mus: 3 np arrays - for the mea, p, and rho parameters for the
            response distribution corresponding to each of N observations. Each numpy array is of
            shape (N,1).
        :type mus: np.ndarray
        :return: a N-dimensional vector containing the log-probability of observing each data-point
            under the current model.
        :rtype: np.ndarray
        """
        mu = robjects.FloatVector(mus[0].flatten().tolist())
        theta = robjects.FloatVector(mus[1].flatten().tolist())
        rho = robjects.FloatVector(mus[2].flatten().tolist())
        ld = self.__mgcv.ldTweedie(robjects.FloatVector(y.flatten().tolist()),
                                   mu=mu,phi=rinterface.NA,
                                   rho=rho,theta=theta,
                                   a=self.a,b=self.b,
                                   **{'all.derivs': True})
        
        ld = np.array(ld)
        return ld[:,0]
    
    def llk(self, y, *mus):
        """log-probability of data under given model. Essentially sum over all elements in the
        vector returned by the :func:`lp` method.

        log-likelihood is computed by ``mgcv``'s ``ldTweedie`` function.

        References:
         - Wood, Pya, & Säfken (2016). Smoothing Parameter and Model Selection for General Smooth \
            Models.
         - Wood, S. N., & Fasiolo, M. (2017). A generalized Fellner-Schall method for smoothing \
            parameter optimization with application to Tweedie location, scale and shape models.
         - ``ldTweedie`` function in ``mgcv``, see: https://github.com/cran/mgcv/blob/master/R/gam.fit3.r#L2838

        :param y: A numpy array containing each observed value.
        :type y: np.ndarray
        :param mus: 3 np arrays - for the mea, p, and rho parameters for the
            response distribution corresponding to each of N observations. Each numpy array is of
            shape (N,1).
        :type mus: np.ndarray
        :return: The log-probability of observing all data under the current model.
        :rtype: float
        """
        return np.sum(self.lp(y,*mus))
    
    def get_resid(self, y, *mus):
        """Get deviance residuals for a Tweedie model.

        Code was taken and adapted to python from the ``residuals`` function of the ``twlss`` family
        implemented in ``mgcv``.

        References:
         - Wood, Pya, & Säfken (2016). Smoothing Parameter and Model Selection for General Smooth \
            Models.
         - Wood, S. N., & Fasiolo, M. (2017). A generalized Fellner-Schall method for smoothing \
            parameter optimization with application to Tweedie location, scale and shape models.
         - ``residuals`` function of the ``twlss`` family in ``mgcv``,\
            see: https://github.com/cran/mgcv/blob/master/R/gamlss.r#L2523

        :param y: A numpy array containing each observed value.
        :type y: np.ndarray
        :param mus: 3 np arrays - for the mea, p, and rho parameters for the
            response distribution corresponding to each of N observations. Each numpy array is of
            shape (N,1).
        :type mus: np.ndarray
        :return: A list of standardized residuals that should be ~ N(0,1) if the model is correct.
        :rtype: np.ndarray
        """
        mu = mus[0]
        theta = mus[1]
        rho = mus[2]
        a = self.a
        b = self.b

        ind = theta > 0
        ethi = np.exp(-theta[ind])
        ethni = np.exp(theta[~ind])
        theta[ind] = (b+a*ethi)/(1+ethi)
        theta[~ind] = (b*ethni+a)/(1+ethni)

        y1 = y + (y == 0).astype(int)
        t = (np.power(y1,1 - theta) - np.power(mu,1 - theta))/(1 - theta)
        k = (np.power(y,2 - theta) - np.power(mu,2 - theta))/(2 - theta)

        rsd = np.sign(y-mu)*np.sqrt(np.maximum(2 * (y * t - k) * 1/rho,0))
        return rsd

    # Methods below are required by abstract class but not needed here, so
    # delegate to super, which will return None
    def lcp(self, y, *mus):
        return super().lcp(y, *mus)
    
    def rvs(self, *mus, size = 1, seed = 0):
        return super().rvs(*mus, size=size, seed=seed)
        