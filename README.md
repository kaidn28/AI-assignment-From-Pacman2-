1. ReflectAgent:
Pacman càng được nhiều điểm nếu càng gần đồ ăn và càng xa con ma
Cách tính điểm cho pacman đối với từng thức ăn sẽ là 1/(food_distance) và từng con ma sẽ là 1/(ghost_distance)
Cặp nhật điểm cho pacman theo food bằng score += alpha x (1/food_distance) 
                      và theo con ma    score -= 1.0 x (1/ghost_distance)
Trong đó đại lượng alpha coi như độ liều lĩnh của pacman, alpha càng lớn thì pacman càng coi trọng việc ăn được thức ăn so với việc tránh con ma

2. MinmaxAgent:

Hàm get_value: Trả về action và score cho action đó
Hàm max_value: Xác định hành động của pacman sao cho đạt được điểm cao nhất
Hàm min_value: Xác định hành động của các con ma sao cho đạt được điểm thấp nhất
