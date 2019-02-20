# =============================================================================
# Event is base class for all subsequent events, that will trigger events
# in the trading infrastructure
# =============================================================================
class Event (object):
    pass

# =============================================================================
# Handles events of receiving a new market update with corresponding bars
# =============================================================================
class MarketEvent (Event):
    def __init__(self):
        self.type = 'MARKET'
        
# =============================================================================
# Handles event of sending Signal from a Strategy object.
# This is received by a Portfolio object and acted upon
# =============================================================================
class SignalEvent (Event):
    """
    Initialised the SignalEvent
    
    Parameters:
        strategy_id: the unique identifier for the strategy that generated
            the signal.
        symbol: the ticker symbol, e.g 'GOOG'
        datetime: the timestamp at which the signal was generated
        signal_type: 'LONG' or 'SHORT'
        strength: an adjustment factor 'suggestion' used to scale quantity
            at the portfolio level. Useful for pairs strategies.
    """
    def __init__(self, strategy_id, symbol, datetime, signal_type, strength):
        self.type = 'SIGNAL'
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength
        
        
"""
Handles the event of sending an Order Event to execution system.
The order contains a symbol (e.g  GOOG), a type (market or limit),
quantity and a direction.
"""
class OrderEvent (Event):
    """
    Initialises the order type, setting whether it is a Market order ('MKT')
    or Limit order ('LMT'), has a quantity (integral) and its direction
    ('BUY' or 'SELL').
    
    Parameters:
        symbol: instrument to trade
        order_type: 'MKT' or 'LMT'
        quantity: non-negative integer
        direction: 'BUY' or 'SELL'
    """
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
        
    def print_order(self):
        print(
            "Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" %
            (self.symbol, self.order_type, self.quantity, self.direction)
            )
        
"""
Encapsulates the notion of Fill order, as returned from a brokerage. 
Stores the quantity of an instrument actually filled and at what price.
In addition, stores the commission of the trade from the brokerage
"""
class FillEvent (Event):
    """
    Initialised the FillEvent object. Sets the symbol, exchange, quantity, 
    direction, cost of fill and an optional commission
    
    If commission is not provided, FillEvent will calculate it based on the 
    trade size and Interactive Brokers fee.
    
    Parameters:
        timeindex: the bar-resolution when the order was filled
        symbol: instrument which was filled
        exchange: the exchange where the order was filled
        quantity: the filled quantity
        direction: the direction of the fill ('BUY' or 'SELL')
        fill_cost: the holdings value in dollars
        commission: an optional commission sent from IB
    """
    def __init__(self, timeindex, symbol, exchange, quantity, direction, 
                 fill_cost, commission=None):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        
        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission
            
    """
    Calculate IB commission based on "US API Directed Orders":
    
    https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2
    """
    def calculate_ib_commission(self):
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013*self.quantity)
        else:
            full_cost = max(1.3, 0.008*self.quantity)
        return full_cost