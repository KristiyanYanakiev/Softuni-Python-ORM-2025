from django.db import models




class RechargeEnergyMixin(models.Model):
    def recharge_energy(self, amount: int):
        self.energy = min(self.energy + amount, 100)
        self.save()

    class Meta:
        abstract = True