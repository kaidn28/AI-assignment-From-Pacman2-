1. ReflectAgent:
Pacman càng được nhiều điểm nếu càng gần đồ ăn và càng xa con ma
Cách tính điểm cho pacman đối với từng thức ăn sẽ là 1/(food_distance) và từng con ma sẽ là 1/(ghost_distance)
Cặp nhật điểm cho pacman theo food bằng score += alpha x (1/food_distance) 
                      và theo con ma    score -= 1.0 x (1/ghost_distance)
Trong đó đại lượng alpha coi như độ liều lĩnh của pacman, alpha càng lớn thì pacman càng coi trọng việc ăn được thức ăn so với việc tránh con ma

2. MinmaxAgent:

Hàm get_value: Trả về action và score cho action đó, gọi hàm max_value nếu agent là pacman, hàm min_value nếu agent là ghost

Đối với pacman:
Hàm max_value: Xác định hành động của pacman sao cho đạt được điểm cao nhất:
  Đầu tiên cho max_value = -inf
  Ở mỗi node, so sánh max value với các successor, thay thế nếu successor_value > max_value và prun nếu gặp successor_value bé hơn, sau đó trả về action

Đối với ghost:
Hàm min_value: Xác định hành động của các con ma sao cho pacman đạt được điểm thấp nhất:
  Đầu tiên cho min_value = inf
  Ở mỗi node, so sánh min_value với các successor, thay thế nếu successor_value <min_value và prun nếu gặp successor_value lớn hơn, sau đó trả về action 


3. AlphaBetaAgent:
Tương tự minimaxAgent, nhưng có thêm alpha và beta.
- Alpha: Giá trị lớn nhất có thể đạt được của maximizer (Pacman)
- Beta: Giá trị bé nhất có thể đạt được của minimizer (Ghost)

Tại mỗi hàm maxValue, so sánh value tìm được với beta. Cắt nhánh nếu value > beta, nếu không thì gán lại alpha = max(alpha, value) Tại mỗi hàm minValue, so sánh value tìm được với alpha. Cắt nhanh nếu value < alpha, nếu không thì gán lại beta = min(beta, value)
