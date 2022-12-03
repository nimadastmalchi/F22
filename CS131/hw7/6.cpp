class Charger {
public:
    virtual void get_power() = 0;
    virtual double get_max_amps() const = 0;
    virtual double check_price_per_kwh() const = 0;
};

class SuperCharger : public Charger {
public:
    void get_power() { ... }
    double get_max_amps() const { ... }
    double check_price_per_kwh() const { ... }
};

class ElectricVehicle {
public:
    void charge(Charger& sc) { ... }
};

class ElectrityPriceCalculator {
    double get_price() const { ... }
};

class SuperCharger {
public:
    void get_power() { ... }
    double get_max_amps() const { ... }
    double check_price_per_kwh(ElectrityPriceCalculator&) const { ... }
};