class Effect:
    def __init__(self, name, target_attribute, modifier_type, value, duration_ticks):
        self.name = name
        self.target_attribute = target_attribute  # Should be a secondary attribute
        self.modifier_type = modifier_type  # "percentage" or "flat"
        self.value = value
        self.duration_ticks = duration_ticks
        self.remaining_ticks = duration_ticks

    def __str__(self):
        return (f"Effect: {self.name} on {self.target_attribute} "
                f"({'+' if self.value >=0 else ''}{self.value}"
                f"{'%' if self.modifier_type == 'percentage' else ''}, "
                f"{self.remaining_ticks}/{self.duration_ticks} ticks left)")