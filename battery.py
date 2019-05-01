class Battery(object):
    """Electric battery operating in price arbitrage.

    power       float [MW] same for charge & discharge
    capacity    float [MWh]
    efficiency  float [%] round trip, applied to
    """

    def __init__(self, power, capacity, efficiency=0.9, state=0):
        self.power = float(power)
        self.capacity = float(capacity)
        self.efficiency = float(efficiency)
        self.state = float(state)
        
        return 
    
    def __str__(self):
        battery_info = f'Battery Summary \nPower Limit: {self.power} \nCapacity: {self.capacity} \nEfficiency: {self.efficiency} \nCharge State: {self.state}'
        
        return battery_info
    
    def charge(self, power, time=1):
        """ Charging the battery
        
        power       float [MW]
        time        float number of hours at the requested power
        """
        
        requested_charge = round((float(power)*float(time)) * self.efficiency, 2)
        requested_state = round(self.state + requested_charge, 2)
        
        ## Checking Constraints
        assert power <= self.power, f'Power requested, {power}, is greater than possible power: {self.power}'
        assert power > 0, f'Power requested for charge, {power}, is negative'
        assert requested_state <= self.capacity, f'Charge requested, {requested_charge}, would leave the battery state, {self.state}, above capacity ({self.capacity}): {requested_state}'
        
        ## Charging
        self.state = requested_state
    
    def discharge(self, power, time=1):
        """ Discharging the battery
        
        power   float [MW]
        time    float number of hours at the requested power
        """
        
        requested_discharge = round(power*time, 2)
        requested_state = round(self.state - requested_discharge, 2)
        
        ## Checking Constraints
        assert power <= self.power, f'Power requested, {power}, is greater than possible power: {self.power}'
        assert power > 0, f'Power requested for discharge, {power}, is negative'
        assert requested_state >= 0, f'Discharge requested, {requested_discharge}, would leave the battery state, {self.state}, below 0: {requested_state}'
        
        ## Discharging
        self.state = requested_state
    