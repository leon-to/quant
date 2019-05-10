from trader2.data import DataHandler

class Backtest:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.r = {} # result
        
    def run(self):
        close = self.data_handler.close
        symbols = self.data_handler.symbols
        
        while True:
            i += 1
            print (i)
            #update the market bars
            if self.data_handler.continue_backtest == True:
                self.data_handler.update_bars()
            else:
                break
            
            #handle events
            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == 'MARKET':
                            self.strategy.calculate_signals(event)
                            self.portfolio.update_timeindex(event)
                        elif event.type == 'SIGNAL':
                            self.signals += 1
                            self.portfolio.update_signal(event)
                        elif event.type == 'ORDER':
                            self.orders += 1
                            self.execution_handler.execute_order(event)
                        elif event.type == 'FILL':
                            self.fills += 1
                            self.portfolio.update_fill(event)
                            
            time.sleep(self.heartbeat)
        