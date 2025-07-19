class Effect:
    def __init__(self, name, target_attribute, modifier_type, value, duration_ticks, dot_damage=0, dot_type=None):
        self.name = name
        self.target_attribute = target_attribute  # Should be a secondary attribute
        self.modifier_type = modifier_type  # "percentage" or "flat"
        self.value = value
        self.duration_ticks = duration_ticks
        self.remaining_ticks = duration_ticks
        self.dot_damage = dot_damage
        self.dot_type = dot_type # e.g., "Poison", "Fire"

    def __str__(self):
        parts = [f"Effect: {self.name}"]
        details = []
        if self.target_attribute:
            mod_str = f"{'+' if self.value >= 0 else ''}{self.value}{'%' if self.modifier_type == 'percentage' else ''}"
            details.append(f"on {self.target_attribute} {mod_str}")
        if self.dot_damage > 0:
            details.append(f"{self.dot_damage} {self.dot_type or 'damage'}/tick")
        if details:
            parts.append(f"[{', '.join(details)}]")

        parts.append(f"({self.remaining_ticks}/{self.duration_ticks} ticks left)")
        return " ".join(parts)