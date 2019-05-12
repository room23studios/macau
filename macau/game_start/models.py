from django.db import models


class Game(models.Model):
    pin = models.IntegerField(unique=True)
    state = models.CharField(max_length=10, default='lobby')

    def __str__(self):
        return "Game: " + str(self.pin) + " " + self.state
