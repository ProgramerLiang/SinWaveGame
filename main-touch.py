"""=========================================="""
"""|          Developed by Corripo          |"""
"""|  Please read README.md before running  |"""
"""|  This is a touchable optimized version |"""
"""=========================================="""
import pygame
import math
import random
import os
import sys
import time

print("==========================================")
print("|          Developed by Corripo          |")
print("|  Please read README.md before running  |")
print("==========================================")

# 初始化配置
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 左侧触控按钮配置
BUTTONS = {
    'A_up':    pygame.Rect(50, 80, 120, 40),
    'A_down':  pygame.Rect(50, 130, 120, 40),
    'ω_up':    pygame.Rect(50, 200, 120, 40),
    'ω_down':  pygame.Rect(50, 250, 120, 40),
    'φ_up':    pygame.Rect(50, 320, 120, 40),
    'φ_down':  pygame.Rect(50, 370, 120, 40),
    'regenerate': pygame.Rect(50, 420, 120, 40)  # 新增重新生成按钮
}

BUTTON_LABELS = {
    'A_up':    "振幅 +",
    'A_down':  "振幅 -",
    'ω_up':    "频率 +",
    'ω_down':  "频率 -",
    'φ_up':    "相位 +",
    'φ_down':  "相位 -",
    'regenerate': "新目标"  # 按钮标签
}

class TouchController:
    def __init__(self):
        self.active_button = None
        self.press_start_time = 0

    def get_speed(self):
        hold_time = time.time() - self.press_start_time
        if hold_time > 2.0: return 5.0
        if hold_time > 1.0: return 3.0
        if hold_time > 0.5: return 2.0
        return 1.0

touch_ctrl = TouchController()

class FontManager:
    def __init__(self):
        self.font = self._load_font()
        
    def _load_font(self):
        try:
            if os.path.exists("DVSMNFPLNXH.ttf"):
                return pygame.font.Font("DVSMNFPLNXH.ttf", 18)
        except Exception as e:
            print(f"字体加载异常: {e}")
        
        for name in ['arial', 'simhei', 'helvetica']:
            try:
                return pygame.font.SysFont(name, 18)
            except: continue
        
        return pygame.font.Font(None, 18)

font_mgr = FontManager()

def draw_grid(surface):
    for x in range(0, WIDTH, 50):
        pygame.draw.line(surface, (220,220,220), (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(surface, (220,220,220), (0,y), (WIDTH,y))

def draw_parameter_panel(surface, font, params, similarity):
    panel = pygame.Surface((250, 180), pygame.SRCALPHA)
    panel.fill((255,255,255,200))
    
    help_text = [
        "操作指南：",
        "短按：微调参数",
        "长按：加速调整"
    ]
    
    y = 8
    for text in help_text:
        panel.blit(font.render(text, True, (80,80,80)), (10, y))
        y += 20
    
    pygame.draw.line(panel, (200,200,200), (10, y), (240, y), 1)
    y += 12
    
    value_info = [
        f"振幅 A: {params['A']:.1f}",
        f"频率 ω: {params['ω']:.3f}",
        f"相位 φ: {params['φ']:.2f}",
        f"匹配度: {similarity:.1f}%"
    ]
    
    for text in value_info:
        panel.blit(font.render(text, True, (0,0,0)), (10, y))
        y += 25
    
    surface.blit(panel, (WIDTH-260, 20))
    
    # 绘制所有按钮
    for name, rect in BUTTONS.items():
        color = (180, 230, 180) if touch_ctrl.active_button == name else (220, 220, 220)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        label = font.render(BUTTON_LABELS[name], True, (0,0,0))
        surface.blit(label, (rect.x + 10, rect.y + 10))

def show_success_dialog(surface, font):
    """改进的成功弹窗，包含确认按钮"""
    dialog_size = (320, 200)
    dialog_rect = pygame.Rect((WIDTH-dialog_size[0])//2, (HEIGHT-dialog_size[1])//2, *dialog_size)
    button_rect = pygame.Rect(dialog_rect.x + 80, dialog_rect.y + 140, 160, 40)

    # 半透明遮罩
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0, 160))
    surface.blit(overlay, (0,0))
    
    # 对话框主体
    pygame.draw.rect(surface, (255,255,255), dialog_rect, border_radius=10)
    text = font.render("匹配成功！", True, (0, 150, 0))
    surface.blit(text, text.get_rect(center=(dialog_rect.centerx, dialog_rect.centery - 30)))
    
    # 确认按钮
    pygame.draw.rect(surface, (100, 200, 100), button_rect, border_radius=5)
    btn_text = font.render("再来一次", True, (0,0,0))
    surface.blit(btn_text, (button_rect.x + 40, button_rect.y + 10))
    
    # 检测点击
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(mouse_pos):
        return True
    return False

def regenerate_target():
    """生成新目标函数并重置参数"""
    global target_params, params
    target_params = {
        'A': random.uniform(30.0, 70.0),
        'ω': random.uniform(0.03, 0.07),
        'φ': random.uniform(-math.pi, math.pi)
    }
    params = {'A':50.0, 'ω':0.05, 'φ':0.0}  # 重置当前参数

# 初始化参数
regenerate_target()  # 初始生成目标
running = True
success = False

# 主循环
while running:
    screen.fill((255, 255, 255))
    draw_grid(screen)
    
    # 绘制波形
    target_points = [(x, HEIGHT//2 + target_params['A']*math.sin(target_params['ω']*x + target_params['φ'])) 
                    for x in range(WIDTH)]
    pygame.draw.lines(screen, (255,0,0), False, target_points, 2)
    
    current_points = [(x, HEIGHT//2 + params['A']*math.sin(params['ω']*x + params['φ'])) 
                     for x in range(WIDTH)]
    pygame.draw.lines(screen, (0,120,255), False, current_points, 3)
    
    # 计算匹配度
    similarity = 100 * (0.4*(1 - abs(params['A']-target_params['A'])/70) +
                       0.4*(1 - abs(params['ω']-target_params['ω'])/0.04) +
                       0.2*(1 - abs(params['φ']-target_params['φ'])/(2*math.pi)))
    similarity = max(0, min(100, similarity))
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 处理所有按下事件
        if event.type in [pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN]:
            pos = (event.x*WIDTH, event.y*HEIGHT) if hasattr(event, 'finger') else pygame.mouse.get_pos()
            
            # 优先检测重新生成按钮
            if BUTTONS['regenerate'].collidepoint(pos):
                regenerate_target()
                success = False
            else:
                for name, rect in BUTTONS.items():
                    if rect.collidepoint(pos) and name != 'regenerate':
                        touch_ctrl.active_button = name
                        touch_ctrl.press_start_time = time.time()
        
        if event.type in [pygame.FINGERUP, pygame.MOUSEBUTTONUP]:
            touch_ctrl.active_button = None
    
    # 参数调整
    if touch_ctrl.active_button:
        base_speed = 1.2
        speed = base_speed * touch_ctrl.get_speed()
        delta = speed * (1/60)
        
        if 'A_up' in touch_ctrl.active_button: params['A'] += delta * 1.5
        if 'A_down' in touch_ctrl.active_button: params['A'] -= delta * 1.5
        if 'ω_up' in touch_ctrl.active_button: params['ω'] += delta * 0.03
        if 'ω_down' in touch_ctrl.active_button: params['ω'] -= delta * 0.03
        if 'φ_up' in touch_ctrl.active_button: params['φ'] += delta * 0.5
        if 'φ_down' in touch_ctrl.active_button: params['φ'] -= delta * 0.5
        
        params['A'] = max(0.1, min(params['A'], 100.0))
        params['ω'] = max(0.001, min(params['ω'], 0.1))
    
    # 成功检测
    if similarity >= 95 and not success:
        success = True
    
    # 显示成功弹窗
    if success:
        if show_success_dialog(screen, font_mgr.font):
            regenerate_target()
            success = False
    
    draw_parameter_panel(screen, font_mgr.font, params, similarity)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
