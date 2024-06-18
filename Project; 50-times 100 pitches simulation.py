import numpy as np

# 투수의 피칭존별 피안타율 및 피홈런률 데이터
pitches_paa = np.array([
    [0.190, 0.205, 0.240, 0.225, 0.190],
    [0.275, 0.300, 0.295, 0.290, 0.225],
    [0.260, 0.305, 0.310, 0.325, 0.230],
    [0.255, 0.290, 0.285, 0.280, 0.205],
    [0.190, 0.235, 0.250, 0.265, 0.140]
])

pitches_iso = np.array([
    [0.005, 0.015, 0.025, 0.005, 0.000],
    [0.015, 0.020, 0.055, 0.030, 0.005],
    [0.005, 0.045, 0.080, 0.035, 0.020],
    [0.015, 0.025, 0.035, 0.025, 0.025],
    [0.010, 0.035, 0.030, 0.055, 0.000]
])

# 타자의 피칭존별 안타 확률
hitting_prob = np.array([
    [0.250, 0.225, 0.310, 0.205, 0.240],
    [0.265, 0.300, 0.315, 0.310, 0.235],
    [0.250, 0.325, 0.350, 0.305, 0.220],
    [0.235, 0.300, 0.305, 0.300, 0.205],
    [0.230, 0.305, 0.300, 0.255, 0.200]
])

# 타자의 피칭존별 홈런 확률
home_run_prob = np.array([
    [0.030, 0.025, 0.020, 0.015, 0.010],
    [0.025, 0.020, 0.015, 0.010, 0.005],
    [0.020, 0.015, 0.010, 0.005, 0.000],
    [0.015, 0.010, 0.005, 0.000, 0.000],
    [0.010, 0.005, 0.000, 0.000, 0.000]
])

# 존 밖으로 볼을 던질 확률
outside_zone_prob = 0.36

def simulate_game(pitches_paa, pitches_iso, hitting_prob, home_run_prob, outside_zone_prob, num_simulations=50):
    total_hits = 0
    total_home_runs = 0
    total_outs = 0
    total_strikeouts = 0
    total_walks = 0
    
    for _ in range(num_simulations):
        pitch_count = 0
        outs = 0
        strikeouts = 0
        walks = 0
        hits = 0
        home_runs = 0
        strikes_in_zone = 0
        balls_outside_zone = 0
        non_strikeout_outs = 0
        
        while pitch_count < 100:
            # 무작위로 투구존 선택
            zone_row = np.random.randint(0, 5)
            zone_col = np.random.randint(0, 5)
            
            # 피안타율 및 피장타율 확인
            paa = pitches_paa[zone_row, zone_col]
            iso = pitches_iso[zone_row, zone_col]
            
            # 안타 발생 여부 결정
            hit = np.random.random() < (hitting_prob[zone_row, zone_col] * (1 - pitches_paa[zone_row, zone_col]))
            if hit:
                hits += 1
                # 홈런 발생 여부 결정
                if np.random.random() < home_run_prob[zone_row, zone_col] * (1 - pitches_iso[zone_row, zone_col]):
                    home_runs += 1
                # 볼카운트 초기화
                strikes_in_zone = 0
                balls_outside_zone = 0
                pitch_count += 1
                continue
            
            # 삼진, 볼넷, 아웃 결정
            if strikes_in_zone < 3:  # 삼진이 되기 위해서는 존 안에 스트라이크 3개가 필요합니다. 
                strikes_in_zone += 1
                if strikes_in_zone == 3:
                    strikeouts += 1
                    # 볼카운트 초기화
                    strikes_in_zone = 0
                    balls_outside_zone = 0
                    pitch_count += 1
                    continue
            else:
                if balls_outside_zone == 4:  # 볼넷이 되기 위해서는 존 밖으로 4번의 볼이 필요합니다.
                    walks += 1
                    # 볼카운트 초기화
                    strikes_in_zone = 0
                    balls_outside_zone = 0
                    pitch_count += 1
                    continue
                else:
                    if np.random.random() < outside_zone_prob:
                        balls_outside_zone += 1
                    else:
                        non_strikeout_outs += 1
                        # 타자가 2스트라이크에서 헛스윙을 하는 경우 삼진 처리
                        if strikes_in_zone == 2:
                            strikeouts += 1
                        # 볼카운트 초기화
                        strikes_in_zone = 0
                        balls_outside_zone = 0
                        pitch_count += 1
                        continue
            
            # 아웃 3회면 루프 종료
            if non_strikeout_outs == 3:
                break
        
        # 전체 통계 누적
        total_hits += hits
        total_home_runs += home_runs
        total_outs += (strikeouts + non_strikeout_outs)
        total_strikeouts += strikeouts
        total_walks += walks
    
    return total_hits, total_home_runs, total_outs, total_strikeouts, total_walks

# 시뮬레이션 실행
total_hits, total_home_runs, total_outs, total_strikeouts, total_walks = simulate_game(pitches_paa, pitches_iso, hitting_prob, home_run_prob, outside_zone_prob)

print(f"50번의 시뮬레이션 결과:")
print(f"총 안타: {total_hits}")
print(f"총 홈런: {total_home_runs}")
print(f"총 아웃: {total_outs}")
print(f"총 삼진: {total_strikeouts}")
print(f"총 볼넷: {total_walks}")
