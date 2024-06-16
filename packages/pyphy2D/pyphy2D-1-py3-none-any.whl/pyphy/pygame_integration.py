import pygame as pg


class PyphyPygame:

    class PyphySurface(pg.Surface):...
    
    @staticmethod
    def DrawCircle(window, color, center, radius) -> None:
        pg.draw.circle(window, color, center, radius)

    @staticmethod
    def DrawLine(window, color, start, end, thickness) -> None:
        pg.draw.line(window, color, start, end, thickness)
    
    @staticmethod
    def DrawPolygon(window, color, vertices) -> None:
        pg.draw.polygon(window, color, vertices)

    @staticmethod
    def RotateImage(image, degree) -> PyphySurface:
        return pg.transform.rotate(image, degree)
    
    @staticmethod
    def Blit(window, surface, position) -> None:
        window.blit(surface, position)

    @staticmethod
    def GetWindowHeight(window) -> int:
        return window.get_height()
    
    @staticmethod
    def GetWindowWidth(window) -> int:
        return window.get_width()
    
    @staticmethod
    def GetWindowSize(window) -> tuple[int, int]:
        return window.get_size()
    
    @staticmethod
    def ScaleImage(image, scale) -> PyphySurface:
        return pg.transform.scale(image, scale)