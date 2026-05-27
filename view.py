import pygame

import config


class Screen:
    def __init__(self):
        self.width = config.DEFAULT_WINDOW_WIDTH
        self.height = config.DEFAULT_WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        pygame.display.set_caption(config.GAME_TITLE)
        self.myfont = pygame.font.Font(None, config.GAME_FONT_SIZE)
        self.title_font = pygame.font.Font(None, config.TITLE_FONT_SIZE)
        self.button_font = pygame.font.Font(None, config.BUTTON_FONT_SIZE)
        self.instruction_font = pygame.font.Font(None, config.INSTRUCTION_FONT_SIZE)

        icon = pygame.image.load(config.ICON_PATH)
        pygame.display.set_icon(icon)

        self.background_image = pygame.image.load(config.BACKGROUND_PATH).convert()
        self.game_width = self.background_image.get_width()
        self.game_height = self.background_image.get_height()
        self.game_scene = pygame.Surface((self.game_width, self.game_height)).convert()
        self.game_rect = None
        self.update_game_rect()

        table_image = pygame.image.load(config.TABLE_PATH).convert_alpha()
        self.table = pygame.transform.scale(table_image, (config.TABLE_WIDTH, config.TABLE_HEIGHT))

        self.person_rect = pygame.Rect(
            config.PERSON_RECT_X,
            config.PERSON_RECT_Y,
            config.PERSON_RECT_WIDTH,
            config.PERSON_RECT_HEIGHT,
        )
        self.instruction_book_rect = pygame.Rect(
            config.INSTRUCTION_BOOK_X,
            config.INSTRUCTION_BOOK_Y,
            config.INSTRUCTION_BOOK_WIDTH,
            config.INSTRUCTION_BOOK_HEIGHT,
        )

        self.menu_buttons = {}
        self.settings_buttons = {}
        self.settings_sliders = {}
        self.update_buttons()

        self.running = True
        self.clock = pygame.time.Clock()

    def set_window_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.update_game_rect()
        self.update_buttons()

    def set_window_mode(self, mode_type: str, width: int, height: int) -> None:
        if mode_type == config.WINDOW_MODE_FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif mode_type == config.WINDOW_MODE_BORDERED_FULLSCREEN:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.update_game_rect()
        self.update_buttons()

    def update_game_rect(self) -> None:
        scale_x = self.width / self.game_width
        scale_y = self.height / self.game_height
        scale = max(scale_x, scale_y)
        new_width = max(config.MIN_SCALED_SIZE, int(self.game_width * scale))
        new_height = max(config.MIN_SCALED_SIZE, int(self.game_height * scale))

        self.game_rect = pygame.Rect(0, 0, new_width, new_height)
        self.game_rect.center = (self.width // 2, self.height // 2)

    def update_buttons(self) -> None:
        self.menu_buttons = {
            config.BUTTON_START: self.create_button(0),
            config.BUTTON_CONTINUE: self.create_button(1),
            config.BUTTON_SETTINGS: self.create_button(2),
            config.BUTTON_EXIT: self.create_button(3),
        }
        self.settings_buttons = {
            config.BUTTON_MUSIC: self.create_settings_button(0),
            config.BUTTON_SOUND: self.create_settings_button(2),
            config.BUTTON_WINDOW_SIZE: self.create_settings_button(4),
            config.BUTTON_BACK: self.create_settings_button(5),
        }
        self.settings_sliders = {
            config.SLIDER_MUSIC_VOLUME: self.create_settings_slider(1),
            config.SLIDER_SOUND_VOLUME: self.create_settings_slider(3),
        }

    def create_button(self, number: int) -> pygame.Rect:
        x = self.width // 2 - config.MENU_BUTTON_WIDTH // 2
        y = config.MENU_FIRST_BUTTON_Y + number * config.MENU_BUTTON_GAP
        return pygame.Rect(x, y, config.MENU_BUTTON_WIDTH, config.MENU_BUTTON_HEIGHT)

    def create_settings_button(self, number: int) -> pygame.Rect:
        x = self.width // 2 - config.MENU_BUTTON_WIDTH // 2
        y = config.SETTINGS_FIRST_BUTTON_Y + number * config.SETTINGS_BUTTON_GAP
        return pygame.Rect(x, y, config.MENU_BUTTON_WIDTH, config.MENU_BUTTON_HEIGHT)

    def create_settings_slider(self, number: int) -> pygame.Rect:
        x = self.width // 2 - config.SLIDER_TRACK_WIDTH // 2
        y = config.SETTINGS_FIRST_BUTTON_Y + number * config.SETTINGS_BUTTON_GAP
        y += config.SLIDER_TRACK_OFFSET_Y
        return pygame.Rect(x, y, config.SLIDER_TRACK_WIDTH, config.SLIDER_TRACK_HEIGHT)

    def draw_menu(self, has_save: bool) -> None:
        self.draw_menu_background()
        self.draw_title(config.MENU_TITLE_TEXT)

        self.draw_button(self.menu_buttons[config.BUTTON_START], config.MENU_START_TEXT)
        self.draw_button(
            self.menu_buttons[config.BUTTON_CONTINUE],
            config.MENU_CONTINUE_TEXT,
            has_save,
        )
        self.draw_button(self.menu_buttons[config.BUTTON_SETTINGS], config.MENU_SETTINGS_TEXT)
        self.draw_button(self.menu_buttons[config.BUTTON_EXIT], config.MENU_EXIT_TEXT)

        self.update_screen()

    def draw_settings(
        self,
        music_enabled: bool,
        sound_enabled: bool,
        music_volume: float,
        sound_volume: float,
        window_mode_text: str,
    ) -> None:
        music_text = self.get_setting_text(config.MUSIC_SETTING_TEXT, music_enabled)
        sound_text = self.get_setting_text(config.SOUND_SETTING_TEXT, sound_enabled)
        music_volume_text = self.get_volume_text(config.MUSIC_VOLUME_TEXT, music_volume)
        sound_volume_text = self.get_volume_text(config.SOUND_VOLUME_TEXT, sound_volume)
        size_text = config.WINDOW_SIZE_TEXT.format(mode=window_mode_text)

        self.draw_menu_background()
        self.draw_title(config.SETTINGS_TITLE_TEXT)

        self.draw_button(self.settings_buttons[config.BUTTON_MUSIC], music_text)
        self.draw_slider(
            self.settings_sliders[config.SLIDER_MUSIC_VOLUME],
            music_volume_text,
            music_volume,
        )
        self.draw_button(self.settings_buttons[config.BUTTON_SOUND], sound_text)
        self.draw_slider(
            self.settings_sliders[config.SLIDER_SOUND_VOLUME],
            sound_volume_text,
            sound_volume,
        )
        self.draw_button(self.settings_buttons[config.BUTTON_WINDOW_SIZE], size_text)
        self.draw_button(self.settings_buttons[config.BUTTON_BACK], config.MENU_BACK_TEXT)

        self.update_screen()

    def draw_game(
        self,
        balance: int,
        instruction_open: bool = False,
        instruction_lines=None,
    ) -> None:
        self.screen.fill(config.MENU_BACKGROUND_COLOR)
        self.draw_game_scene()

        scaled_scene = pygame.transform.scale(self.game_scene, self.game_rect.size)
        self.screen.blit(scaled_scene, self.game_rect)
        self.draw_balance(balance)

        if instruction_open:
            self.draw_instruction(instruction_lines)

        self.update_screen()

    def draw_game_scene(self) -> None:
        self.game_scene.blit(self.background_image, (config.BACKGROUND_X, config.BACKGROUND_Y))
        pygame.draw.rect(self.game_scene, config.PERSON_COLOR, self.person_rect)
        self.game_scene.blit(self.table, (config.TABLE_X, config.TABLE_Y))

    def draw_menu_background(self) -> None:
        self.screen.fill(config.MENU_BACKGROUND_COLOR)

    def draw_balance(self, balance: int) -> None:
        text = config.BALANCE_TEXT.format(balance=balance)
        label = self.myfont.render(text, True, config.BALANCE_TEXT_COLOR)
        label_rect = label.get_rect(topleft=(config.BALANCE_X, config.BALANCE_Y))

        self.screen.blit(label, label_rect)

    def draw_instruction(self, instruction_lines) -> None:
        if instruction_lines is None:
            instruction_lines = []

        panel = pygame.Rect(0, 0, config.INSTRUCTION_PANEL_WIDTH, config.INSTRUCTION_PANEL_HEIGHT)
        panel.center = (self.width // 2, self.height // 2)

        pygame.draw.rect(self.screen, config.INSTRUCTION_PANEL_COLOR, panel)
        pygame.draw.rect(self.screen, config.INSTRUCTION_BORDER_COLOR, panel, 2)

        title = self.button_font.render(config.INSTRUCTION_TITLE_TEXT, True, config.INSTRUCTION_TEXT_COLOR)
        title_rect = title.get_rect(center=(panel.centerx, panel.y + config.INSTRUCTION_PANEL_PADDING))
        self.screen.blit(title, title_rect)

        x = panel.x + config.INSTRUCTION_PANEL_PADDING
        y = panel.y + config.INSTRUCTION_TITLE_GAP
        max_width = panel.width - config.INSTRUCTION_PANEL_PADDING * 2

        for line in instruction_lines:
            wrapped_lines = self.wrap_text(line, self.instruction_font, max_width)
            for wrapped_line in wrapped_lines:
                text = self.instruction_font.render(wrapped_line, True, config.INSTRUCTION_TEXT_COLOR)
                self.screen.blit(text, (x, y))
                y += self.instruction_font.get_height() + config.INSTRUCTION_LINE_GAP

            y += config.INSTRUCTION_LINE_GAP

    def draw_title(self, text: str) -> None:
        title = self.title_font.render(text, True, config.MENU_TEXT_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, config.TITLE_Y))
        self.screen.blit(title, title_rect)

    def draw_button(self, rect: pygame.Rect, text: str, enabled: bool = True) -> None:
        mouse_pos = pygame.mouse.get_pos()
        color = config.BUTTON_COLOR
        text_color = config.BUTTON_TEXT_COLOR

        if not enabled:
            color = config.BUTTON_DISABLED_COLOR
            text_color = config.BUTTON_DISABLED_TEXT_COLOR
        elif rect.collidepoint(mouse_pos):
            color = config.BUTTON_HOVER_COLOR

        pygame.draw.rect(self.screen, color, rect)

        label = self.button_font.render(text, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def draw_slider(self, rect: pygame.Rect, text: str, value: float) -> None:
        label = self.button_font.render(text, True, config.BUTTON_TEXT_COLOR)
        label_rect = label.get_rect(center=(self.width // 2, rect.y - config.SLIDER_LABEL_OFFSET_Y))
        self.screen.blit(label, label_rect)

        pygame.draw.rect(self.screen, config.SLIDER_TRACK_COLOR, rect)

        fill_width = int(rect.width * value)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(self.screen, config.SLIDER_FILL_COLOR, fill_rect)

        knob_x = rect.x + fill_width
        knob = pygame.Rect(0, 0, config.SLIDER_KNOB_WIDTH, config.SLIDER_KNOB_HEIGHT)
        knob.center = (knob_x, rect.centery)
        pygame.draw.rect(self.screen, config.SLIDER_KNOB_COLOR, knob)

    def get_setting_text(self, template: str, enabled: bool) -> str:
        if enabled:
            state = config.SETTING_ON_TEXT
        else:
            state = config.SETTING_OFF_TEXT

        return template.format(state=state)

    def get_volume_text(self, template: str, volume: float) -> str:
        volume_percent = int(volume * config.VOLUME_PERCENT)
        return template.format(volume=volume_percent)

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list:
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if current_line == "":
                new_line = word
            else:
                new_line = current_line + " " + word

            if font.size(new_line)[0] <= max_width:
                current_line = new_line
            else:
                if current_line != "":
                    lines.append(current_line)
                current_line = word

        if current_line != "":
            lines.append(current_line)

        return lines

    def get_game_mouse_pos(self, mouse_pos):
        if not self.game_rect.collidepoint(mouse_pos):
            return None

        game_x = int((mouse_pos[0] - self.game_rect.x) * self.game_width / self.game_rect.width)
        game_y = int((mouse_pos[1] - self.game_rect.y) * self.game_height / self.game_rect.height)

        return game_x, game_y

    def is_instruction_book_clicked(self, mouse_pos) -> bool:
        game_pos = self.get_game_mouse_pos(mouse_pos)

        if game_pos is None:
            return False

        return self.instruction_book_rect.collidepoint(game_pos)

    def update_screen(self) -> None:
        pygame.display.update()
        self.clock.tick(60)
