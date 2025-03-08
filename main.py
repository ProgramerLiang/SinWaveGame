"""=========================================="""
"""|          Developed by Corripo          |"""
"""|  Please read README.md before running  |"""
"""| Double-click 双击运行.bat to run program |"""
"""=========================================="""
import pygame
import math
import random
import os

print("==========================================")
print("|          Developed by Corripo          |")
print("|  Please read README.md before running  |")
print("==========================================")

# 初始化配置
pygame.init()
WIDTH, HEIGHT = 900, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class FontManager:
    def __init__(self):
        self.font = self._load_font()
        
    def _load_font(self):
        """字体加载策略"""
        try:
            if os.path.exists("DVSMNFPLNXH.ttf"):
                return pygame.font.Font("DVSMNFPLNXH.ttf", 16)
        except Exception as e:
            print(f"字体加载异常: {e}")
        
        for name in ['arial', 'simhei', 'helvetica']:
            try:
                return pygame.font.SysFont(name, 16)
            except:
                continue
        
        return pygame.font.Font(None, 16)

font_mgr = FontManager()

def draw_grid(surface):
    """绘制等间距网格"""
    for x in range(0, WIDTH, 50):
        pygame.draw.line(surface, (220,220,220), (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(surface, (220,220,220), (0,y), (WIDTH,y))

def draw_parameter_panel(surface, font, params, similarity):
    """显示参数面板"""
    panel = pygame.Surface((220, 150), pygame.SRCALPHA)
    panel.fill((255,255,255,180))
    
    # 函数公式显示
    formula_text = [
        "波形函数:",
        "y = A·sin(ωx + φ)"
    ]
    
    # 参数数值显示
    value_info = [
        f"振幅 A: {params['A']:.1f}",
        f"频率 ω: {params['ω']:.3f}",
        f"相位 φ: {params['φ']:.2f}",
        f"匹配度: {similarity:.1f}%"
    ]
    
    y = 8
    for text in formula_text:
        text_surf = font.render(text, True, (0,0,0))
        panel.blit(text_surf, (10, y))
        y += 20
    
    # 分隔线
    pygame.draw.line(panel, (200,200,200), (10, y), (210, y), 1)
    y += 10
    
    for text in value_info:
        text_surf = font.render(text, True, (0,0,0))
        panel.blit(text_surf, (10, y))
        y += 20
    
    surface.blit(panel, (WIDTH-230, 20))

def show_success_dialog(surface, font):
    """显示成功对话框"""
    dialog_size = (300, 150)
    dialog_rect = pygame.Rect(
        (WIDTH - dialog_size[0])//2, 
        (HEIGHT - dialog_size[1])//2,
        dialog_size[0],
        dialog_size[1]
    )
    
    # 半透明遮罩
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0, 128))
    surface.blit(overlay, (0,0))
    
    # 对话框主体
    pygame.draw.rect(surface, (255,255,255), dialog_rect, border_radius=8)
    
    # 文字内容
    text = font.render("匹配成功！", True, (0,200,0))
    text_rect = text.get_rect(center=(dialog_rect.centerx, dialog_rect.top + 40))
    surface.blit(text, text_rect)
    
    # 确认按钮
    button_rect = pygame.Rect(
        dialog_rect.centerx - 60,
        dialog_rect.bottom - 60,
        120,
        40
    )
    pygame.draw.rect(surface, (0,150,0), button_rect, border_radius=5)
    btn_text = font.render("确认 (Enter)", True, (255,255,255))
    surface.blit(btn_text, btn_text.get_rect(center=button_rect.center))
    
    return button_rect

def generate_wave(params):
    """生成波形坐标点"""
    return [(x, params['A']*math.sin(params['ω']*x + params['φ']) + HEIGHT//2) 
            for x in range(WIDTH)]

def generate_target():
    """生成目标波形参数"""
    return {
        'A': 50.0 + random.random() * 150,
        'ω': 0.02 + random.random() * 0.1,
        'φ': random.uniform(0, 2*math.pi)
    }

def calculate_similarity(player, target):
    """计算波形匹配度"""
    total_error = sum(abs(p[1]-t[1]) for p,t in zip(player, target))
    max_error = 2 * HEIGHT * len(player)
    return max(0, 100 - (total_error / max_error * 100))

# 全局参数初始化
params = {'A': 100.0, 'ω': 0.05, 'φ': 0.0}
target = generate_target()
target_points = generate_wave(target)

def main():
    global target, target_points
    player_points = generate_wave(params)
    running = True
    show_dialog = False
    stored_similarity = 0

    # 控制配置（修改后的键位）
    key_config = {
        pygame.K_UP:    {'param':'A', 'step':3.0},
        pygame.K_DOWN:  {'param':'A', 'step':-3.0},
        pygame.K_LEFT:  {'param':'ω', 'step':0.001},
        pygame.K_RIGHT: {'param':'ω', 'step':-0.001},
        pygame.K_a:     {'param':'φ', 'step':0.1},   # A键增加相位
        pygame.K_d:     {'param':'φ', 'step':-0.1}   # D键减少相位
    }

    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # R键重置
                    target = generate_target()
                    target_points = generate_wave(target)
                if event.key == pygame.K_ESCAPE:  # ESC键退出
                    running = False
                if show_dialog and event.key == pygame.K_RETURN:  # 回车确认
                    show_dialog = False
                    target = generate_target()
                    target_points = generate_wave(target)
                
            if event.type == pygame.MOUSEBUTTONDOWN and show_dialog:
                if dialog_button.collidepoint(event.pos):
                    show_dialog = False
                    target = generate_target()
                    target_points = generate_wave(target)

        # 参数更新逻辑
        if not show_dialog:
            keys = pygame.key.get_pressed()
            for key in key_config:
                if keys[key]:
                    cfg = key_config[key]
                    params[cfg['param']] += cfg['step']

            # 参数范围限制
            params['A'] = max(10.0, min(params['A'], 300.0))
            params['ω'] = max(0.01, min(params['ω'], 0.2))
            
            # 生成玩家波形
            player_points = generate_wave(params)
            current_similarity = calculate_similarity(player_points, target_points)
            
            # 触发成功对话框
            if current_similarity >= 95:
                stored_similarity = current_similarity
                show_dialog = True

        # 画面渲染
        screen.fill((255,255,255))
        draw_grid(screen)
        pygame.draw.lines(screen, (0,0,255), False, target_points, 2)
        pygame.draw.lines(screen, (255,0,0), False, player_points, 2)
        
        # 显示参数面板
        draw_parameter_panel(screen, font_mgr.font, params, 
                            stored_similarity if show_dialog else current_similarity)
        
        # 显示对话框
        if show_dialog:
            dialog_button = show_success_dialog(screen, font_mgr.font)
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
