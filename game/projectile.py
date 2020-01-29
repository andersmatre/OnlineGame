
from pygame import gfxdraw
import math


class Projectile:

    def __init__(self, x, y, goal, size=10, dmg=1, speed=0.5):
        self.x = x
        self.y = y

        self.goal = goal
        self.change = self.change()

        self.speed = speed
        self.size = size
        self.dmg = dmg

    def change(self):
        vec_x = self.goal[0] - self.x
        vec_y = self.goal[1] - self.y
        vec_length = math.sqrt(vec_x ** 2 + vec_y ** 2)
        vec_x /= vec_length
        vec_y /= vec_length
        return [vec_x, vec_y]

    def collisions(self, client, projectiles):
        # Remove if outside of screen.
        if not 0 < self.x < client.width and not 0 < self.y < client.height:
            projectiles.remove(self)

        # Check for collisions with other players
        for q in client.get_queue[0]:
            dist = math.hypot(self.x - q.x, self.y - q.y)
            if dist < self.size + q.size:
                projectiles.remove(self)
                client.player.hit.update({q: self.dmg})

    def update(self, client, projectiles):
        self.collisions(client, projectiles)
        self.x += self.change[0] * self.speed * client.dt
        self.y += self.change[1] * self.speed * client.dt

    def draw(self, screen):
        gfxdraw.aacircle(screen, round(int(self.x)), round(int(self.y)), self.size, (0, 0, 0))
        gfxdraw.filled_circle(screen, round(int(self.x)), round(int(self.y)), self.size, (0, 0, 0))
