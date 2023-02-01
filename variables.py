
lottery_guru_url = 'https://lotteryguru.com/ontario-lottery-results'

olg_link = 'https://www.olg.ca/en/home.html'

lottery_names = [
    "Lotto Max",
    "Lotto 6/49",
    "Lottario",
    "Ontario 49",
    "Keno",
    "Pick 4",
    "Pick 3",
    "Encore"
]

lottery_with_bonus = [
    "Lotto Max",
    "Lotto 6/49",
    "Lottario",
    "Ontario 49",
]

lottery_order_matters = [
    "Pick 3",
    "Pick 4",
    "Encore"
]

lottery_facts = {
    "Lotto Max" : {"value_range" : [1,50], "numbers_drawn":7, 'numbers_repeated':False,
                   'image_file':'lotto_max.png', 'colors':['#F2F2F2', '#84bd00', '#0085c7' '#6C736F' ]},

    "Lotto 6/49":{"value_range" : [1,49], "numbers_drawn":6,'numbers_repeated':False,
                  'image_file':'lotto_649.png','colors':['#F2F2F2', '#82A3FF', '#FF4D4D', '#6C736F']},

    "Lottario":{"value_range" : [1,45], "numbers_drawn":6,'numbers_repeated':False,
                'image_file':'lottario.png', 'colors':['#F2F2F2','#ffc11c', '#f22a3f', '#6C736F']},

    "Ontario 49":{"value_range" : [1,49], "numbers_drawn":6,'numbers_repeated':False,
                  'image_file':'ontario_49.png', 'colors':['#F2F2F2', '#cc212d', '#6C736F' ]},

    "Keno":{"value_range" : [1,70], "numbers_drawn":20,'numbers_repeated':False,
            'image_file':'keno.png', 'colors':['#F2F2F2', '#F0B74D', '#02A161', '#6C736F']},

    "Pick 4":{"value_range" : [1,9], "numbers_drawn":4,'numbers_repeated':True,
              'image_file':'pick_4.png', 'colors':['#F2F2F2','#E6CF00', '#6C736F']},

    "Pick 3":{"value_range" : [1,9], "numbers_drawn":3,'numbers_repeated':True,
              'image_file':'pick_3.png', 'colors':['#F2F2F2','#f22a3f', '#6C736F']},

    "Encore":{"value_range" : [1,9], "numbers_drawn":7, 'numbers_repeated':True,
              'image_file':'encore.png', 'colors':['#F2F2F2','#2271D5', '#6C736F']}
}

number_keys = [
    'number_1',
    'number_2',
    'number_3',
    'number_4',
    'number_5',
    'number_6',
    'number_7'
]
