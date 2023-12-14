# как пользоваться:
# label start:
    # camera at parallax

# в настройках можно добавить:
# textbutton _("Параллакс") action Parallax()

# для смены со вспышкой:
# textbutton _("Параллакс") action Parallax(True)

# переключатель на экране preferences в файле screens.rpy:
# vbox:
    # style_prefix "check"
    # label _("Параллакс")
    # textbutton _("Вкл/Выкл") action Parallax()

# фоны всегда должны начинаться с bg и пробела, иначе не сработает

init offset = -2

# переключение параллакса в настройках
default persistent.parallax = True

# плавность: ближе к 0 - медленнее, ближе к 1 - быстрее
define par_easing_factor = 0.05

# ДАЛЬШЕ НИЧЕГО МЕНЯТЬ НЕ СТОИТ

# по умолчанию спрайты расположены близко, а задний фон - далеко
define config.default_transform = near
define config.tag_transform = { "bg": far }

init -3 python:
    # для фона
    def far_f(trans, st, at):
        trans.zpos = -750 if persistent.parallax else 0
        trans.zoom = 1.035 if persistent.parallax else 1
        return 1 / 30.

    # для спрайтов
    def near_f(trans, st, at):
        trans.ypos = int(config.screen_height * .528) if persistent.parallax else int(config.screen_height * .5)
        return 1 / 30.

init -3:
    # трансформ для камеры с параллаксом
    transform parallax:
        perspective True
        subpixel True
        function moving_camera

    # плавно отключить смещения
    transform parallax_off:
        perspective True
        subpixel True
        ease .25 xoffset 0 yoffset 0

    # смещаем спрайт немного вниз, чтобы эффект параллакса не показывал его обрезку
    transform near:
        truecenter()
        function near_f

    # немного увеличиваем и отдаляем фон, чтобы не видеть его краёв при смещении
    transform far:
        truecenter()
        zzoom True
        function far_f

# плавное смещение камеры, которое зависит от курсора
init -3 python:
    def moving_camera(trans, st, at):
        if persistent.parallax:
            x, y = renpy.display.draw.get_mouse_pos()
            
            parallax_factor = par_easing_factor
            target_xoffset = (x - config.screen_width / 2) * parallax_factor
            target_yoffset = (y - config.screen_height / 2) * parallax_factor
            
            easing_factor = par_easing_factor
            trans.xoffset += (target_xoffset - trans.xoffset) * easing_factor
            trans.yoffset += (target_yoffset - trans.yoffset) * easing_factor
        else:
            trans.xoffset = 0
            trans.yoffset = 0
        
        return 0

    # класс для переключения параллакса
    class Parallax(Action):
        def __init__(self, blink=False):
            self.blink = blink
            if persistent.parallax is None:
                persistent.parallax = True

        def __call__(self):
            persistent.parallax = not persistent.parallax
            if self.blink:
                if persistent.parallax:
                    renpy.transition(Fade(.075, 0, .075, color="#f45"))
                else:
                    renpy.transition(Fade(.075, 0, .075, color="#2b7"))
            renpy.restart_interaction()

        def get_selected(self):
            return persistent.parallax

