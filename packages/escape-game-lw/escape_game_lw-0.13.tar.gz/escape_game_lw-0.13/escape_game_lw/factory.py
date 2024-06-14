import itertools

class order():
  id_iter = itertools.count()
  def __init__(self, time_step :int, order : dict):
    self.order_time = time_step
    self.arrival_time = time_step + 50
    self.completed = False
    self.order_id = next(self.id_iter)

    # validate order: colors
    for key in order:
      if key not in ['red','yellow','white','blue']:
        raise ValueError(f"The color {key} can't be ordererd. ")
    # validate order: sum
    sum_material = sum([order[color] for color in order])
    if sum_material > 300:
      raise ValueError(f"The total amount of material per order should not exceed 300. You ordered {sum_material} in total.")

    # add colors if missing to dict
    for color in ['blue', 'yellow', 'red','white']:
      if color not in order.keys():
          order[color] = 0 
    self.order_dict = order

  def set_completed(self):
    self.completed = True
    print(f"Order {self.order_id} arrived.")
    
    
cups_recipes = {'cup_rose' : {'material' : {
                            'red' : 0.5,
                            'blue' : 0,
                            'white' : 0.5,
                            'yellow' : 0,
                            },
                            'batch_duration' : 4,
                            'batch_size' : 2,
                            'batch_material' : 8,
                            },
            'cup_orange' : {'material' : {
                                'red' : 0.4,
                                'blue' : 0,
                                'white' : 0.2,
                                'yellow' : 0.4,
                            },
                            'batch_duration' : 3,
                            'batch_size' : 3,
                            'batch_material' : 10
                },
            'cup_purple' : {'material' : {
                                'red' : 0.4,
                                'blue' : 0.5,
                                'white' : 0.1,
                                'yellow' : 0,
                            },
                            'batch_duration' : 10,
                            'batch_size' : 4,
                            'batch_material' : 20
            },
            'cup_multicolor' : {'material' : {
                                'red' : 0.2,
                                'blue' : 0.3,
                                'white' : 0.2,
                                'yellow' : 0.3,
                            },
                            'batch_duration' : 50,
                            'batch_size' : 15,
                            'batch_material' : 50
            }
            
    }

class factory_machine():
  __time_shift = 800
  __order_limit = 2

  def __init__(self, case=1):
    self.time = 0
    self.product = None
    self._output = {r : 0 for r in cups_recipes.keys()}
    self._orders = []
    self._machine_fill= {
                  'red' : 0,
                  'blue' : 0,
                  'white' : 0,
                  'yellow' : 0,
    }
    self._stock = {
                  'red' : 100,
                  'blue' : 100,
                  'white' : 100,
                  'yellow' : 100,
    }
    self.done = False

  def check_machine_ready(self, product : str) -> bool: 
    """ checks if machine is ready to product the product

      product(str) Name of product. In this case the color of the cup

      returns True if the relative amount of granulate is suited for the production
    """
    try:
      recipe_color = cups_recipes[product]
    except:
      raise ValueError(f'The recipe for the product {product} could not be found')

    machine_material_sum = sum([self._machine_fill[color] for color in self._machine_fill])
    if machine_material_sum == 0:
      rel_material = {color : 0 for color in self._machine_fill}
    else:
      rel_material = {color : self._machine_fill[color]/machine_material_sum for color in self._machine_fill}

    # check if ratio is correct
    return min([rel_material[color] == recipe_color['material'][color] for color in rel_material]) == 1

  def check_output(self) -> dict:
    """checks the current output of the machine"""
    return self._output

  def check_machine_fill(self) -> dict:
    """checks the current fill of the machine"""
    return self._machine_fill

  def check_stock(self) -> dict:
    """checks the current stock besides the machine"""
    return self._stock

  def switch_off(self):
    """ turns machine off"""
    print("(!) end of shift")
    self.done = True

  def __pass_time(self, amount : int) -> bool:
    """logic for time steps, check if order arrived 
      amount (int) : amount of time units to add to time
    """
    
    if self.done:
      return False
    
    self.time = self.time + amount
    
    if self.time >= self.__time_shift:
        self.switch_off()

    for i in range(len(self._orders)):
        order = self._orders[i]
        if not order.completed:
            if self.time >= order.arrival_time:
                new_fill = {color : self._stock[color] + order.order_dict[color] for color in self._stock}
                self._stock  = new_fill
                self._orders[i].completed = True
                print(f"... order {order.order_id} arrived in material stock of the machine.")
    return True
                       
  def wait(self, time_units):
    if time_units >= 0:
      self.__pass_time(time_units)
    else:
      raise ValueError("Can wait for positive time units only.")
    
  def set_product(self, product : str):
    if product in cups_recipes.keys():
      self.product = product
    else:
      print(f"Product {product} not found in available recipes")
      
    self._machine_fill= {
                  'red' : 0,
                  'blue' : 0,
                  'white' : 0,
                  'yellow' : 0,
    }
    time_step = 40
    
    print("(!) changed product; machine needs to be filled for production start.")
    self.__pass_time(time_step)

  def produce(self, cycles=1):
    """
      produce if possible cycles * batch_size of products.
      time spent is calculated by cycles * duration of product
      material required is calculated by cycles * batch_material
    """
    if self.done:
        self.switch_off()
        return False
    
    # check the requirements
    if self.product is None:
      print("Nothing to produce. Please set a product")
      return False
    else:
      if not self.check_machine_ready(self.product):
        print("Machine not ready. The material is not matching the product recipe.",
              "Did you select the correct product?")
        return False

    recipe_product = cups_recipes[self.product]
    time_needed = recipe_product['batch_duration'] * cycles
    material_needed = {color : recipe_product['material'][color] * recipe_product['batch_material'] * cycles for color in recipe_product['material']}
    output_produced = cycles * recipe_product['batch_size']
    # check if enough time 
    if (time_needed + self.time) > self.__time_shift:
      raise ValueError(f"The time needed for {cycles} cycles is {time_needed}.",
                       f"This will exceed the shift duration by {(time_needed + self.time) - self.__time_shift} time units.")

    # check if enough material
    for color in material_needed:
      if self._machine_fill[color] < (material_needed[color]):
        raise ValueError(f"Not enough material for color {color}. {material_needed[color]} needed and only {self._machine_fill[color]} in machine left.")

    # produce
    new_fill = {color : self._machine_fill[color] - material_needed[color] for color in self._machine_fill}
    self._machine_fill  = new_fill
    self.__pass_time(time_needed)

    self._output[self.product] = self._output[self.product] + output_produced
    print(f"... produced {output_produced} products of '{self.product}'.")

    return True

  def time_until_next_order(self):
    for i in range(len(self._orders)):
        order = self._orders[i]
        if not order.completed:
            return (order.arrival_time - self.time)
    print("(!) time until next order couldn't be calculated because there is no order pending")
    return 0
          
  def count_active_order(self):
      return sum([1 for order in self._orders if not order.completed])
    
  def print_machine_status(self):
    print('*************************************************************')
    print(f'current time    : {self.time}')
    print(f'current product : {self.product}\n')
    print(f'-- material in machine')
    for color in self._machine_fill:
        print(f'{color.ljust(10)} : {self._machine_fill[color]}')
    print('\n')
    print(f'-- refill stock next to machine')
    for color in self._stock:
        print(f'{color.ljust(10)} : {self._stock[color]}')
    print('\n')
    print(f'-- current output this shift')
    for out in self._output:
        print(f'{out.ljust(15)} : {self._output[out]}')
    print('\n')
    print(f'-- current orders')
    print(f'active orders  : {sum([1 for order in self._orders if not order.completed])}')
    print(f'arrived orders : {sum([1 for order in self._orders if order.completed])}')
    print('*************************************************************')

  def order_material(self, order_dict):
    new_order = order(self.time, order_dict)
    
    if sum([1 for o in self._orders if not o.completed]) == self.__order_limit:
        print(f"(!) order not accepted; order limit is {self.__order_limit}")
        return False
    else:
        self._orders.append(new_order)
        return True

  def fill_machine(self, amount_dict):
    if self.done:
        self.switch_off()
        return False
    
    time_step = 5
    
    # create a complete dictionary
    for color in ['blue', 'yellow', 'red','white']:
      if color not in amount_dict.keys():
          amount_dict[color] = 0 

    # check if amount is more than stock
    if min({amount_dict[color] <= self._stock[color] for color in amount_dict}) != 1:
      raise ValueError("You want to fill more in your machine then the stock at the machine side can provide. Order material first ")

    # add to machine & remove from stock
    machine_fill = {color : int(self._machine_fill[color] + amount_dict[color]) for color in self._machine_fill}
    self._machine_fill  = machine_fill
    stock_fill = {color : int(self._stock[color] - amount_dict[color]) for color in self._machine_fill}
    self._stock = stock_fill

    # pass time
    self.__pass_time(time_step)
    return True
  
  
