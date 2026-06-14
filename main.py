import pygame

from utils.settings import *

from entities.enemies.basic_enemy import BasicEnemy
from entities.enemies.fast_enemy import FastEnemy
from entities.enemies.tank_enemy import TankEnemy
from entities.towers.basic_tower import BasicTower
from entities.towers.sniper_tower import SniperTower
from entities.towers.splash_tower import SplashTower
from systems.wave_parameters import WAVES
from systems.game_reset import GameReset
from systems.main_menu import MainMenu
from systems.radial_menu import RadialMenu, RadialMenuOption
from systems.menu import Menu

pygame.init()
pygame.display.set_caption("Iron Dome")
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

clock = pygame.time.Clock()

runtime_settings = {
    "FPS": FPS,
    "GRID_SIZE": GRID_SIZE,
    "STARTING_METAL": STARTING_METAL,
    "STARTING_HEALTH": STARTING_HEALTH
}
game_reset = GameReset(SCREEN_WIDTH, SCREEN_HEIGHT, WAVES)


def unpack_state(state):
    return (
        state["path_tiles"],
        state["grid"],
        state["path"],
        state["wave_manager"],
        state["enemies"],
        state["towers"],
        state["projectiles"],
        state["metal"],
        state["player_health"],
        state["enemies_killed"]
    )


game_state = game_reset.create_state(
    runtime_settings["STARTING_METAL"],
    runtime_settings["STARTING_HEALTH"],
    runtime_settings["GRID_SIZE"]
)
(
    path_tiles,
    grid,
    path,
    wave_manager,
    enemies,
    towers,
    projectiles,
    metal,
    player_health,
    enemies_killed
) = unpack_state(game_state)

game_over_started_at = None


def reset_progress():
    state = game_reset.create_state(
        runtime_settings["STARTING_METAL"],
        runtime_settings["STARTING_HEALTH"],
        runtime_settings["GRID_SIZE"]
    )
    return (*unpack_state(state), None)


def draw_game_over(screen):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 30)

    title = title_font.render("Game Over", True, (255, 90, 90))
    title_rect = title.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 - 28)
    )
    screen.blit(title, title_rect)

    subtitle = small_font.render(
        "Resetting progress...",
        True,
        (235, 235, 245)
    )
    subtitle_rect = subtitle.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + 32)
    )
    screen.blit(subtitle, subtitle_rect)


def create_tower_option(label, tower_class, color, icon_path, enabled=True):
    modifier_stats = [
        f"{tag}: {modifier:+} damage"
        for tag, modifier in tower_class.tag_damage_modifiers.items()
    ]

    if not modifier_stats:
        modifier_stats = ["Modifiers: None"]

    return RadialMenuOption(
        label,
        color,
        icon_path=icon_path,
        value_text=str(tower_class.cost),
        stats=[
            f"Cost: {tower_class.cost} metal",
            f"Damage: {tower_class.damage}",
            f"Range: {tower_class.range_radius}",
            f"Fire rate: {tower_class.fire_rate}",
            *modifier_stats
        ],
        info_text=tower_class.info,
        payload=tower_class,
        enabled=enabled
    )


def create_enemy_option(label, enemy_class, color):
    return RadialMenuOption(
        label,
        color,
        icon_path=f"assets/{enemy_class.sprite_file}",
        value_text=f"{enemy_class.health} HP",
        stats=[
            f"Health: {enemy_class.health}",
            f"Speed: {enemy_class.speed}",
            f"Metal drop: {enemy_class.metal_reward}",
            f"Tags: {', '.join(enemy_class.tags)}"
        ],
        info_text=enemy_class.info
    )


menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
main_menu = MainMenu(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    runtime_settings
)
radial_menu = RadialMenu()
build_options = [
    create_tower_option(
        "Basic",
        BasicTower,
        (55, 120, 210),
        "assets/Gatling_Turret_Laser.png"
    ),
    create_tower_option(
        "Splash",
        SplashTower,
        (205, 120, 55),
        "assets/Cannon_Turret_Launcher.png"
    ),
    create_tower_option(
        "Sniper",
        SniperTower,
        (105, 190, 130),
        "assets/Sniper_Turret_Laser.png"
    )
]
enemy_options = [
    create_enemy_option(
        "Basic",
        BasicEnemy,
        (170, 85, 85)
    ),
    create_enemy_option(
        "Fast",
        FastEnemy,
        (180, 155, 70)
    ),
    create_enemy_option(
        "Tank",
        TankEnemy,
        (125, 125, 145)
    )
]

running = True

while running:

    clock.tick(runtime_settings["FPS"])

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_over_started_at is not None:
                    continue

                if radial_menu.is_open:
                    radial_menu.close()
                else:
                    main_menu.toggle()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over_started_at is not None:
                continue

            mouse_pos = event.pos
            gx, gy = grid.world_to_grid(mouse_pos)

            if (
                main_menu.main_button_contains(mouse_pos)
                or main_menu.is_open
            ):
                radial_menu.close()
                action = main_menu.handle_click(mouse_pos)

                if action == "restart":
                    (
                        path_tiles,
                        grid,
                        path,
                        wave_manager,
                        enemies,
                        towers,
                        projectiles,
                        metal,
                        player_health,
                        enemies_killed,
                        game_over_started_at
                    ) = reset_progress()

                continue

            if menu.wave_button_clicked(
                mouse_pos,
                wave_manager.cleared_wave
            ):
                radial_menu.close()
                wave_manager.start_next_wave()
                continue

            if menu.wave_button_contains(mouse_pos):
                radial_menu.close()
                continue

            selected_option = radial_menu.get_selected_option(mouse_pos)

            if selected_option and selected_option.payload:
                tower_class = selected_option.payload
                if metal >= tower_class.cost:
                    wx, wy = radial_menu.world_pos
                    towers.append(
                        tower_class(wx, wy)
                    )
                    metal -= tower_class.cost
                    grid.place(*radial_menu.grid_pos)
                    radial_menu.close()
                continue

            if radial_menu.grid_pos == (gx, gy):
                radial_menu.close()
                continue

            if radial_menu.contains(mouse_pos):
                continue

            wx, wy = grid.grid_to_world(
                gx,
                gy,
                clamp=True
            )

            if (gx, gy) in grid.path_tiles:
                radial_menu.open(
                    (gx, gy),
                    (wx, wy),
                    screen.get_size(),
                    enemy_options
                )
            elif grid.can_place(gx, gy):
                affordable_build_options = [
                    create_tower_option(
                        option.label,
                        option.payload,
                        option.color,
                        option.icon_path,
                        enabled=metal >= option.payload.cost
                    )
                    for option in build_options
                ]

                radial_menu.open(
                    (gx, gy),
                    (wx, wy),
                    screen.get_size(),
                    affordable_build_options
                )
            else:
                radial_menu.close()

    if (
        game_over_started_at is None
        and not main_menu.is_open
    ):
        wave_manager.update(enemies, path)

        for enemy in enemies:
            enemy.update()

        for tower in towers:
            tower.update(enemies, projectiles)

        for projectile in projectiles:
            projectile.update()

        for enemy in enemies:
            if enemy.reached_end and not enemy.metal_collected:
                player_health -= enemy.metal_reward
                enemy.metal_collected = True
            elif not enemy.alive and not enemy.metal_collected:
                metal += enemy.metal_reward
                enemies_killed += 1
                enemy.metal_collected = True

        enemies = [
            e for e in enemies
            if e.alive
        ]
        wave_manager.check_cleared_wave(enemies)

        projectiles = [
            p for p in projectiles
            if p.active
        ]

        if player_health <= 0:
            player_health = 0
            game_over_started_at = pygame.time.get_ticks()
            radial_menu.close()
            main_menu.close()

    if game_over_started_at is not None:
        elapsed_time = pygame.time.get_ticks() - game_over_started_at

        if elapsed_time >= 3000:
            (
                path_tiles,
                grid,
                path,
                wave_manager,
                enemies,
                towers,
                projectiles,
                metal,
                player_health,
                enemies_killed,
                game_over_started_at
            ) = reset_progress()

    screen.fill(BACKGROUND_COLOR)

    grid.draw(
        screen,
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    for enemy in enemies:
        enemy.draw(screen)

    for tower in towers:
        tower.draw(screen)

    for projectile in projectiles:
        projectile.draw(screen)

    menu.draw(
        screen,
        wave_manager.current_wave_number,
        enemies_killed,
        metal,
        BasicTower.cost,
        player_health,
        wave_manager.cleared_wave,
        wave_manager.all_waves_complete
    )

    radial_menu.draw(screen, pygame.mouse.get_pos())
    main_menu.draw_button(screen)
    main_menu.draw_overlay(screen)

    if game_over_started_at is not None:
        draw_game_over(screen)

    pygame.display.flip()

pygame.quit()
