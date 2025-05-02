import random

def random_state(num_queen):
    state = []
    for _ in range(num_queen):
        random_position = random.randint(0, num_queen - 1)
        state.append(random_position)
    return state

def main_evaluation(state, evaluation_type):
    if evaluation_type == 0:
        return first_evaluation(state)
    elif evaluation_type == 1:
        return second_evaluation(state)
    elif evaluation_type == 2:
        return third_evaluation(state)
    

def first_evaluation(state):
  n = len(state)
  num_conflicts = 0
  for i in range(n):
    for j in range(i+1, n):
      if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                num_conflicts += 1

  return num_conflicts

def second_evaluation(state):
  n = len(state)
  row_conflicts_set = set()
  diagonal_conflicts_set = set()
  for i in range(n):
    for j in range(i+1, n):
        if state[i] == state[j]:
          row_conflicts_set.add(state[i])

  for i in range(n):
    for j in range(i+1, n):
        if abs(state[i] - state[j]) == abs(i - j):
          diagonal_conflicts_set.add(state[i])

  row_diagonal_conflicts = len(row_conflicts_set) + len(diagonal_conflicts_set)
  return row_diagonal_conflicts

def third_evaluation(state):
  n = len(state)
  count_conflict = 0
  queens_conflicts = []
  for i in range(n):
    queen = state[i]
    for j in range(n):
      if (state[i] == state[j] and i != j) or (abs(state[i] - state[j]) == abs(i - j) and i != j):
        count_conflict +=1
    queens_conflicts.append(count_conflict)
    count_conflict = 0

  return queens_conflicts

def probability(fitness_list):
    #Calculate probability
    probability_list = []
    sum_fitness = 0
    for i in range(len(fitness_list)):
      sum_fitness += fitness_list[i]

    for k in range(len(fitness_list)):
       probability = fitness_list[k] / sum_fitness
       probability_list.append(probability)

    return probability_list

def probability_ranges(probability_list):
    probability_ranges_list = [0]
    for p in range(len(probability_list)-1):
        probability_ranges_list.append(probability_list[p] + probability_ranges_list[p])
    probability_ranges_list.append(1.0)
    probability_ranges_list.remove(0)
    return probability_ranges_list


def select_population(population, probability_list, probability_ranges_list):
  selected_population = []
  for _ in range(len(population)):
    rndm = random.random()
    selected_chromosome = None
    for q in range(len(probability_ranges_list)):
        if rndm <= probability_ranges_list[q]:
          selected_chromosome = population[q]
          break
      
    selected_population.append(selected_chromosome)
  return selected_population


def crossover(first_state, second_state):
  random_number = random.randint(0, len(first_state) - 1)
  first_part_first_child = first_state[0 : random_number]
  second_part_first_child = second_state[random_number : ]
  first_part_second_child = second_state[0 : random_number]
  second_part_second_child = first_state[random_number :]
  first_child = first_part_first_child + second_part_first_child
  second_child = first_part_second_child + second_part_second_child
  return first_child, second_child


def crossover_population(selected_population):
  new_population = []
  for d in range(0, len(selected_population), 2):
    if d == (len(selected_population) - 1):
       break
    e, f = crossover(selected_population[d], selected_population[d+1])
    new_population.append(e)
    new_population.append(f)

  return new_population


def mutation(chromosome):
  probability_m = 0.05
  random_number_genes = []
  for i in range(len(chromosome)):
    random_p = random.random()
    random_number_genes.append(random_p)

  for j in range(len(chromosome)):
    if random_number_genes[j] < probability_m:
      chromosome[j] = random.randint(0, len(chromosome) - 1)

  return chromosome


def mutate_population(crossovered_population):
  final_population = []
  for t in range(len(crossovered_population)):
        g = mutation(crossovered_population[t])
        final_population.append(g)

  return final_population
    

def genetic(num_queen, num_population, evaluation_type, num_repetition):
    population = []

    #define initial states randomly and saving in the population
    for _ in range(num_population):
        states = []
        for _ in range(num_queen):
            initial_state = random.randint(0, num_queen - 1)
            states.append(initial_state)
        population.append(states)

    #defining fitness function for each evaluation
    #First evaluation
    if evaluation_type == 0:


        for a in range(num_repetition):
            fitness_list = []
            total_pair_queens = num_queen * (num_queen-1) / 2
  
            if a == 0:
                for b in range (num_population):
                    if main_evaluation(population[b], evaluation_type) == 0:
                        return population[b], main_evaluation(population[b], evaluation_type), 0
                
                for c in range(num_population):
                    fitness = total_pair_queens - main_evaluation(population[c], evaluation_type)
                    fitness_list.append(fitness)

                #Calculate probability
                probability_list = probability(fitness_list)
                probability_ranges_list = probability_ranges(probability_list)
                #Generated populations based on probabilities
                selected_population = select_population(population, probability_list, probability_ranges_list)
                crossovered_population = crossover_population(selected_population)
                mutated_population = mutate_population(crossovered_population)
                mutated_population_evaluation = []
                for h in range(len(mutated_population)):
                    mutated_population_evaluation.append(main_evaluation(mutated_population[h], 0))

                for l in range(len(mutated_population_evaluation)):
                    if mutated_population_evaluation[l] == 0:
                      return mutated_population[l], main_evaluation(mutated_population[l], 1), a
                
                if a ==num_repetition:
                   return mutated_population, mutated_population_evaluation
            
        
        

            else:
                for d in range(len(mutated_population)):
                    fitness = total_pair_queens - main_evaluation(mutated_population[d], evaluation_type)
                    fitness_list.append(fitness)
                
                #Calculate probability
                probability_list = probability(fitness_list)
                probability_ranges_list = probability_ranges(probability_list)
                #Generated populations based on probabilities
                selected_population = select_population(mutated_population, probability_list, probability_ranges_list)
                crossovered_population = crossover_population(selected_population)
                mutated_population = mutate_population(crossovered_population)
                mutated_population_evaluation = []

                for h in range(len(mutated_population)):
                   mutated_population_evaluation.append(main_evaluation(mutated_population[h], 0))
                
                for l in range(len(mutated_population_evaluation)):
                   if mutated_population_evaluation[l] == 0:
                      return mutated_population[l], main_evaluation(mutated_population[l], 0), a
                if a == num_repetition -1:
                   return mutated_population, mutated_population_evaluation
                


    elif evaluation_type == 1:
       
        for a in range(num_repetition):
            fitness_list = []
            total_pair_queens = 3 * num_queen - 2
            #calculate Fitness
            if a == 0:
                for b in range (num_population):
                    if main_evaluation(population[b], evaluation_type) == 0:
                        return population[b], main_evaluation(population[b], evaluation_type), 0
                
                for c in range(num_population):
                    fitness = total_pair_queens - main_evaluation(population[c], evaluation_type)
                    fitness_list.append(fitness)

                #Calculate probability
                probability_list = probability(fitness_list)
                probability_ranges_list = probability_ranges(probability_list)
                #Generated populations based on probabilities
                selected_population = select_population(population, probability_list, probability_ranges_list)
                crossovered_population = crossover_population(selected_population)
                mutated_population = mutate_population(crossovered_population)
                mutated_population_evaluation = []
                for h in range(len(mutated_population)):
                   mutated_population_evaluation.append(main_evaluation(mutated_population[h], 1))

                for l in range(len(mutated_population_evaluation)):
                    if mutated_population_evaluation[l] == 0:
                      return mutated_population[l], main_evaluation(mutated_population[l], 1), a
                      
                    
                if a ==num_repetition:
                   return mutated_population, mutated_population_evaluation

        
        

            else:
                for d in range(len(mutated_population)):
                    fitness = total_pair_queens - main_evaluation(mutated_population[d], evaluation_type)
                    fitness_list.append(fitness)
                
                #Calculate probability
                probability_list = probability(fitness_list)
                probability_ranges_list = probability_ranges(probability_list)
                #Generated populations based on probabilities
                selected_population = select_population(mutated_population, probability_list, probability_ranges_list)
                crossovered_population = crossover_population(selected_population)
                mutated_population = mutate_population(crossovered_population)
                mutated_population_evaluation = []

                for h in range(len(mutated_population)):
                   mutated_population_evaluation.append(main_evaluation(mutated_population[h], 1))
                
                for l in range(len(mutated_population_evaluation)):
                   if mutated_population_evaluation[l] == 0:
                      return mutated_population[l], main_evaluation(mutated_population[l], 1), a
                if a == num_repetition -1:
                   return mutated_population, mutated_population_evaluation
                

    elif evaluation_type == 2:


        for a in range(num_repetition):
            fitness_list = []
            total_pair_queens = num_queen * (num_queen-1)
            population_evaluation = []
            for r in range(num_population):
                all_conflicts = 0
                conflicts_list = main_evaluation(population[r], evaluation_type)
                for s in range(num_queen):
                    all_conflicts += conflicts_list[s]
                population_evaluation.append(all_conflicts)
            #calculate Fitness
            if a == 0:
                for b in range (num_population):
                    if population_evaluation[b] == 0:
                        return population[b], main_evaluation(population[b], evaluation_type), 0
                
                for c in range(num_population):
                    fitness = total_pair_queens - population_evaluation[c]
                    fitness_list.append(fitness)

                #Calculate probability
                probability_list = probability(fitness_list)
                probability_ranges_list = probability_ranges(probability_list)
                #Generated populations based on probabilities
                selected_population = select_population(population, probability_list, probability_ranges_list)
                crossovered_population = crossover_population(selected_population)
                mutated_population = mutate_population(crossovered_population)
                mutated_population_evaluation = []
                for r in range(len(mutated_population)):
                  all_conflicts = 0
                  conflicts_list = main_evaluation(mutated_population[r], evaluation_type)
                  for s in range(num_queen):
                    all_conflicts += conflicts_list[s]
                  mutated_population_evaluation.append(all_conflicts)
                
                for l in range(len(mutated_population_evaluation)):
                    if mutated_population_evaluation[l] == 0:
                      return mutated_population[l], main_evaluation(mutated_population[l], 1), a
                
                if a ==num_repetition:
                   return mutated_population, mutated_population_evaluation
            
        
        

            else:
                mutated_population_evaluation = []
                for r in range(len(mutated_population)):
                  all_conflicts = 0
                  conflicts_list = main_evaluation(mutated_population[r], evaluation_type)
                  for s in range(num_queen):
                    all_conflicts += conflicts_list[s]
                  mutated_population_evaluation.append(all_conflicts)

                for d in range(len(mutated_population)):
                    fitness = total_pair_queens - mutated_population_evaluation[d]
                    fitness_list.append(fitness)
                
                #Calculate probability
                probability_list = probability(fitness_list)
                probability_ranges_list = probability_ranges(probability_list)
                #Generated populations based on probabilities
                selected_population = select_population(mutated_population, probability_list, probability_ranges_list)
                crossovered_population = crossover_population(selected_population)
                mutated_population = mutate_population(crossovered_population)
                mutated_population_evaluation = []
                
                for r in range(len(mutated_population)):
                  all_conflicts = 0
                  conflicts_list = main_evaluation(mutated_population[r], evaluation_type)
                  for s in range(num_queen):
                    all_conflicts += conflicts_list[s]
                  mutated_population_evaluation.append(all_conflicts)
                
                for l in range(len(mutated_population_evaluation)):
                    if mutated_population_evaluation[l] == 0:
                      return mutated_population[l], main_evaluation(mutated_population[l], 1), a
                    
                if a == num_repetition -1:
                   return mutated_population, mutated_population_evaluation
                
def generate_neighbors(board):
    neighbors = []
    n = len(board)
    for i in range(n):
        for j in range(n):
            if j != board[i]:
                neighbor = list(board)
                neighbor[i] = j
                neighbors.append(neighbor)
    return neighbors

def best_neighbor(neighbors, evaluation_type, num_random_restart, num_sideway_move, allow_sideways=True):
    
    if evaluation_type == 0:
       
        #best_states = []
        state = neighbors.pop(-1)
        for a in range(num_random_restart):
            fitness_list = []
            total_pair_queens = num_queen * (num_queen-1) / 2
            fitness_state = total_pair_queens - main_evaluation(state, evaluation_type)

            if main_evaluation(state, evaluation_type) == 0:
              '''
              answer = []
              answer.append(state)
              answer.append(main_evaluation(state, evaluation_type))
              answer.append(num_random_restart+1)
              return answer
              '''
              return state, main_evaluation(state, evaluation_type), num_random_restart
            
            for c in range(len(neighbors)):
                    fitness = total_pair_queens - main_evaluation(neighbors[c], evaluation_type)
                    fitness_list.append(fitness)

            best_fitness = max(fitness_list)
            if best_fitness > fitness_state:
               state = neighbors[fitness_list.index(max(fitness_list))]
               neighbors = generate_neighbors(state)
               #break
            
            elif allow_sideways and best_fitness == fitness_state:
                
                temporary_state = neighbors[fitness_list.index(max(fitness_list))]
                temporary_neighbor = generate_neighbors(temporary_state)
                i = 0
                while allow_sideways:
                    if i == num_sideway_move:
                       allow_sideways = False

                    fitness_temporary_state = total_pair_queens - main_evaluation(temporary_state, evaluation_type)
                    temporary_fitness_list = []

                    for d in range(len(temporary_neighbor)):
                        fitness = total_pair_queens - main_evaluation(temporary_neighbor[d], evaluation_type)
                        temporary_fitness_list.append(fitness)

                    temporary_best_fitness = max(temporary_fitness_list)
                    if temporary_best_fitness > fitness_temporary_state:
                      state = temporary_neighbor[temporary_fitness_list.index(max(temporary_fitness_list))]
                      neighbors = generate_neighbors(state)
                      allow_sideways = False

                    elif  temporary_best_fitness == fitness_temporary_state:
                        temporary_state = temporary_neighbor[temporary_fitness_list.index(max(temporary_fitness_list))]
                        temporary_neighbor = generate_neighbors(temporary_state)
                        
                        

                    else:
                       return temporary_state, main_evaluation(temporary_state, evaluation_type), num_random_restart
                    
                    i+=1
                    if num_sideway_move == i:
                       allow_sideways = False
                       return temporary_state, main_evaluation(temporary_state, evaluation_type), num_random_restart
                       
            else:
                return state, main_evaluation(state, evaluation_type), num_random_restart


            if a == num_random_restart-1:
                return state, main_evaluation(state, evaluation_type), num_random_restart+1
              
                  

         
         

    elif evaluation_type == 1:
      #best_states = []
        state = neighbors.pop(-1)
        for a in range(num_random_restart):
            fitness_list = []
            total_pair_queens = 3 * num_queen - 2
            fitness_state = total_pair_queens - main_evaluation(state, evaluation_type)

            if main_evaluation(state, evaluation_type) == 0:
              '''
              answer = []
              answer.append(state)
              answer.append(main_evaluation(state, evaluation_type))
              answer.append(num_random_restart+1)
              return answer
              '''
              return state, main_evaluation(state, evaluation_type), num_random_restart
            
            for c in range(len(neighbors)):
                fitness = total_pair_queens - main_evaluation(neighbors[c], evaluation_type)
                fitness_list.append(fitness)

            best_fitness = max(fitness_list)
            if best_fitness > fitness_state:
              state = neighbors[fitness_list.index(max(fitness_list))]
              neighbors = generate_neighbors(state)
              #break
            
            elif allow_sideways and best_fitness == fitness_state:
                
                temporary_state = neighbors[fitness_list.index(max(fitness_list))]
                temporary_neighbor = generate_neighbors(temporary_state)
                i = 0
                while allow_sideways:
                    if i == num_sideway_move:
                       allow_sideways = False

                    fitness_temporary_state = total_pair_queens - main_evaluation(temporary_state, evaluation_type)
                    temporary_fitness_list = []

                    for d in range(len(temporary_neighbor)):
                        fitness = total_pair_queens - main_evaluation(temporary_neighbor[d], evaluation_type)
                        temporary_fitness_list.append(fitness)

                    temporary_best_fitness = max(temporary_fitness_list)
                    if temporary_best_fitness > fitness_temporary_state:
                      state = temporary_neighbor[temporary_fitness_list.index(max(temporary_fitness_list))]
                      neighbors = generate_neighbors(state)
                      allow_sideways = False

                    elif  temporary_best_fitness == fitness_temporary_state:
                        temporary_state = temporary_neighbor[temporary_fitness_list.index(max(temporary_fitness_list))]
                        temporary_neighbor = generate_neighbors(temporary_state)
                        
                        

                    else:
                       return temporary_state, main_evaluation(temporary_state, evaluation_type), num_random_restart
                    
                    i+=1
                    if num_sideway_move == i:
                       allow_sideways = False
                       return temporary_state, main_evaluation(temporary_state, evaluation_type), num_random_restart
                       
            else:
                return state, main_evaluation(state, evaluation_type), num_random_restart


            if a == num_random_restart-1:
                return state, main_evaluation(state, evaluation_type), num_random_restart+1
     
        '''
      fitness_list = []
      total_pair_queens = 3 * num_queen - 2

      for c in range(len(neighbors)):
            fitness = total_pair_queens - main_evaluation(neighbors[c], evaluation_type)
            fitness_list.append(fitness)
            '''

    elif evaluation_type == 2:
        #best_states = []
        state = neighbors.pop(-1)
        for a in range(num_random_restart):
            fitness_list = []
            total_pair_queens = num_queen * (num_queen-1)
            conflict = 0 
            conflicts_list = main_evaluation(state, evaluation_type)
            for s in range(len(conflicts_list)):
                conflict += conflicts_list[s]

            fitness_state = total_pair_queens - conflict

            if main_evaluation(state, evaluation_type) == 0:
                return state, main_evaluation(state, evaluation_type), num_random_restart
            
            for c in range(len(neighbors)):
                    conflict_neighbor = 0 
                    for r in range(len(neighbors)):
                      conflicts_neighbor_list = main_evaluation(neighbors[r], evaluation_type)
                      for s in range(len(conflicts_neighbor_list)):
                          conflict_neighbor += conflicts_neighbor_list[s]
                      
                      fitness = total_pair_queens - conflict_neighbor
                      fitness_list.append(fitness)
                      conflict_neighbor =0

            best_fitness = max(fitness_list)
            if best_fitness > fitness_state:
               state = neighbors[fitness_list.index(max(fitness_list))]
               neighbors = generate_neighbors(state)
               #break
            
            elif allow_sideways and best_fitness == fitness_state:
                
                temporary_state = neighbors[fitness_list.index(max(fitness_list))]
                temporary_neighbor = generate_neighbors(temporary_state)
                i = 0
                while allow_sideways:
                    if i == num_sideway_move:
                       allow_sideways = False

                    fitness_temporary_state = 0 
                    temporary_conflicts_list = main_evaluation(temporary_state, evaluation_type)
                    for s in range(len(temporary_conflicts_list)):
                        fitness_temporary_state += temporary_conflicts_list[s]

                    fitness_temporary_state = total_pair_queens - fitness_temporary_state
                    temporary_fitness_list = []

                    for d in range(len(temporary_neighbor)):
                                temporary_conflict_neighbor = 0 
                                temporary_conflicts_neighbor_list = main_evaluation(temporary_neighbor[d], evaluation_type)
                                for s in range(len(temporary_conflicts_neighbor_list)):
                                    temporary_conflict_neighbor += temporary_conflicts_neighbor_list[s]
                                fitness = total_pair_queens - temporary_conflict_neighbor
                                temporary_fitness_list.append(fitness)
                                temporary_conflict_neighbor = 0
                                

                    temporary_best_fitness = max(temporary_fitness_list)
                    if temporary_best_fitness > fitness_temporary_state:
                      state = temporary_neighbor[temporary_fitness_list.index(max(temporary_fitness_list))]
                      neighbors = generate_neighbors(state)
                      allow_sideways = False

                    elif  temporary_best_fitness == fitness_temporary_state:
                        temporary_state = temporary_neighbor[temporary_fitness_list.index(max(temporary_fitness_list))]
                        temporary_neighbor = generate_neighbors(temporary_state)
                        
                        

                    else:
                       return temporary_state, main_evaluation(temporary_state, evaluation_type), num_random_restart
                    
                    i+=1
                    if num_sideway_move == i:
                       allow_sideways = False
                       return temporary_state, main_evaluation(temporary_state, evaluation_type), num_random_restart
                       
            else:
                return state, main_evaluation(state, evaluation_type), num_random_restart

                
            if a == num_random_restart-1:
                return state, main_evaluation(state, evaluation_type), num_random_restart+1
                          

        '''  
      fitness_list = []
      total_pair_queens = num_queen * (num_queen-1)
      for c in range(len(neighbors)):
            fitness = total_pair_queens - main_evaluation(neighbors[c], evaluation_type)
            fitness_list.append(fitness)
            '''

def hill_climbing(num_queen, num_random_restart, num_sideway_move, evaluation_type):
    state = random_state(num_queen)
    neighbors = generate_neighbors(state)
    neighbors.append(state)
    best_neighbor_output = best_neighbor(neighbors, evaluation_type, num_random_restart, num_sideway_move, allow_sideways=True)
    return state,neighbors,best_neighbor_output



num_queen = int(input("Please enter the number of queens:"))

#0 = num of total conflicts, 1 = num of conflicted rows and cols, 2 = num of each queens' conflict
evaluation_type = int(input('Please enter the type of evaluatin:'))

#0 = simiulated annealing, 1 = genetic
algorithm_type = int(input('Please enter the type of algorithm:'))

#Hill cimbing algorithm
num_random_restart = int(input('Please enter the number of random restarts:'))
num_sideway_move = int(input('Please enter the number of sideway moves:'))
hill_climbing_algorithm = hill_climbing(num_queen, num_random_restart, num_sideway_move, evaluation_type)
if algorithm_type == 0:
    print("Try another way! it is not defined.")
elif algorithm_type == 1:
    num_population = int(input("Please enter the even number of initial states:"))
    num_repetition = int(input("Please enter the number of repetitions:"))
    genetic_algorithm = genetic(num_queen, num_population, evaluation_type, num_repetition)


#evaluation = main_evaluation(state, evaluation_type)
print(num_queen)
print(evaluation_type)
print(algorithm_type)
#print(genetic_algorithm)
print(hill_climbing_algorithm)
