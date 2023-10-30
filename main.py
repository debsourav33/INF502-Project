

def print_stat(seq1, seq2, score, comparison, shift, chain=False):
    print('')
    print(f'For Shift: {shift}')  
    #print('')
    print('  '.join(seq1))
    print('  '.join(seq2))
    print('  '.join(comparison))
    #print('')
    if chain:
        print(f'Score (longest chain): {score}')
    else:
        print(f'Score (no. of matches): {score}')
    print('')

#length is the minimum length of seq1 or seq2 after shifting either of them (and inserting " " in the shifted cells)
def find_match(seq1,seq2,length, shift):  #shift is only for printing
    comparison = ''
    match = 0

    for i in range(0,length):
        if seq1[i] == seq2[i]:
            match += 1
            comparison += seq1[i]
        else:
            comparison += ' '

    print_stat(seq1,seq2,match,comparison,shift)
    return match

#length is the minimum length of seq1 or seq2 after shifting either of them (and inserting " " in the shifted cells)
def find_chain(seq1,seq2,length, shift):
    
    longest_chain = 0
    match = 0

    chain_start_idx = 0
    
    for i in range(0,length):
        if seq1[i] == seq2[i]:
            match += 1
            if match > longest_chain:
                chain_start_idx = i-match+1
                longest_chain = match
        else:
            match = 0

    comparison = ' ' * chain_start_idx + seq1[chain_start_idx : chain_start_idx+longest_chain]
    print_stat(seq1,seq2,longest_chain,comparison,shift, chain=True)
    return longest_chain

def find_match_by_shifting_seq1(seq1, seq2, max_shift, min_shift = 0, chain = False):
    max_score = 0
    for shift in range(min_shift,max_shift+1):
        shifted_seq1 = ' ' * shift + seq1

        smaller_length = min(len(shifted_seq1), len(seq2))
        
        #chain or subsequence?
        if chain:
            score = find_chain(shifted_seq1,seq2,smaller_length, shift)    
        else:
            score = find_match(shifted_seq1,seq2,smaller_length, shift)
        max_score = max(max_score, score)

        #print(f'For shift {shift}, score: {score}')
    return max_score

def find_match_by_shifting_seq2(seq1, seq2, max_shift, min_shift = 0, chain = False):
    max_score = 0
    for shift in range(min_shift,max_shift+1):
        shifted_seq2 = " " * shift + seq2

        smaller_length = min(len(shifted_seq2), len(seq1))
        
        #chain or subsequence?
        if chain:
            score = find_chain(seq1, shifted_seq2,smaller_length, shift)
        else:
            score = find_match(seq1, shifted_seq2,smaller_length, shift)
        max_score = max(max_score, score)

        #print(f'For shift {shift}, score: {score}')
    return max_score

def pre_process(sequence):
    nucleos = ['A','C','T','G','H']
    sequence = sequence.upper()

    processed = ''

    for char in sequence:
        if char in nucleos:
            processed += char
        
    return processed

def file_input():
    sequence_one = ''
    sequence_two = ''

    while len(sequence_one) == 0:
        print('')
        
        file_seq1 = input("File name containing sequence one: ")
        file_seq1.strip() #strip trailing and leading whitespaces

        try:
            with open(file_seq1,"r") as file:
                lines = file.readlines()
                if len(lines) == 0:
                    print('File must contain the DNA sequence!')
                else:
                    sequence_one = lines[0][:-1] #trim the new line
                    sequence_one = pre_process(sequence_one)
                    if sequence_one=='':
                        print('Sequence must contain atleast one nucleotyde')
                
        except FileNotFoundError:
            print(f"The file {file_seq1} doesn't exist!")

    while len(sequence_two) == 0:
        file_seq2 = input("File name containing sequence two: ")
        file_seq2.strip() #strip trailing and leading whitespaces
        try:
            with open(file_seq2,"r") as file:
                lines = file.readlines()
                if len(lines) == 0:
                    print('File must contain the DNA sequence!')
                else:
                    sequence_two = lines[0][:-1] #trim the new line
                    sequence_two = pre_process(sequence_two)
                    if sequence_two=='':
                        print('Sequence must contain atleast one nucleotyde')
                
        except FileNotFoundError:
            print(f"The file {file_seq2} doesn't exist!")

    print('')
    return sequence_one, sequence_two

def console_input():
    sequence_1 = ''
    sequence_2 = ''

    print('')
    while sequence_1 == '':
        sequence_1 = input("Enter the first sequence: ").strip()
        sequence_1 = pre_process(sequence_1)
        if sequence_1 == '':
            print('Sequence must have atleast one nucleotide')

    while sequence_2 == '':
        sequence_2 = input("Enter the second sequence: ").strip()
        sequence_2 = pre_process(sequence_2)
        if sequence_2== '':
            print('Sequence must have atleast one nucleotide')
    print('')

    return sequence_1, sequence_2

def menu_input():
    print('')
    print("Hello! Welcome to DNA Sequence Matching Program :-)")    

    print('')
    print("How do you want to input the pair of sequence?")
    print('')

    input_choice = -1

    while input_choice!=1 and input_choice!=2:
        try:
            print('')
            print('Console Input    (1)')
            print('File Input       (2)')
            print('')
            input_choice = int(input())
            if input_choice!=1 and input_choice!=2:
                print('The options are 1 or 2!')
        except ValueError:
            print('Entered value is not an integer number!')       

    if input_choice == 1:
        sequence1, sequence2 = console_input() 
    else:
        sequence1, sequence2 = file_input()

    print("---------------------------")
    print("The pair of sequences:\n")
    print(sequence1)
    print(sequence2)
    print("---------------------------")
    
    max_shift = -1
    min_length = min(len(sequence1), len(sequence2))

    print("How much maximum shifts do you want?")

    while max_shift < 0:
        try:
            print('')
            print('Auto adjustment (= length of smallest sequence)       (0)')
            print('Custom Counts                                         (Any Positive Number)')
            print('')
            max_shift = int(input())
            if max_shift < 0:
                print('Max shift count must be non-negative!')
            elif max_shift == 0 or max_shift > min_length:
                max_shift = min_length
                print(f'Max shift is auto adjusted to {max_shift}')
            else: 
                print(f'Max shift is set to {max_shift}')
        except ValueError:
            print('Max shift count must be an integer number!')       
    print('')

    return max_shift, sequence1, sequence2

def menu_operation():
    print('')
    print('Which operation do you want to perform?')
    print('')

    opt = -1

    while opt<0 or opt>5:
        print('')
        print('Find the highest no. of matches without shifting        (1)')
        print('Find the longest contiguous chain without shifting      (2)')
        print('Find the highest no. of matches with shifts done        (3)')
        print('Find the longest contiguous chain with shifts done      (4)')
        print('Exit                                                    (0)')
        print('')

        try:
            opt = int(input())

            if opt <0 or opt>4:
                print('')
                print('Please pick an option between 0 and 4')
                print('')
        except ValueError:
                opt = -1
                print('Please enter an integer number between 0 and 4')

    return opt

def main():
    max_shift, sequence_one, sequence_two = menu_input()

    opt = menu_operation()

    while opt != 0:
        if opt == 1:
            print('')
            print('Trying to find pairwise alignments without any shifting')
            print('')

            #Calculate and print back the count of matches without any shifts done
            no_shift_match = find_match_by_shifting_seq1(sequence_one, sequence_two, max_shift=0)

            print('')
            print(f'Highest no. of matches without shifting: {no_shift_match}')
            print('')

        if opt == 2:
            print('')
            print('Trying to find longest contiguous chain without any shifting')
            print('')

            no_shift_chain = find_match_by_shifting_seq1(sequence_one, sequence_two, max_shift=0, chain=True)

            print('')
            print(f'Length of longest contiguous chain without shifting: {no_shift_chain}')
            print('')

        if opt == 3:
            #Calculate and print back the chain after shifts done with maximum score from sequences
            print('')
            print('Trying to find pairwise alignments with shifting')
            print('')

            shift_seq1_match = find_match_by_shifting_seq1(sequence_one, sequence_two, max_shift= max_shift, min_shift=1)
            shift_seq2_match = find_match_by_shifting_seq2(sequence_one, sequence_two, max_shift= max_shift, min_shift=1)
            max_match = max(shift_seq1_match, shift_seq2_match)

            print('')
            print(f'Highest no. of matches across all possible shifting: {max_match}')
            print('')

        if opt == 4:

            print('')
            print('Trying to find longest contiguous chain with shifting')
            print('')

            #Calculate and print back the maximum contiguous chain (after shifts done ) from sequences
            shift_seq1_chain = find_match_by_shifting_seq1(sequence_one, sequence_two, max_shift= max_shift, min_shift=1, chain=True)
            shift_seq2_chain = find_match_by_shifting_seq2(sequence_one, sequence_two, max_shift= max_shift, min_shift=1, chain=True)
            longest_chain = max(shift_seq1_chain, shift_seq2_chain)

            print('')
            print(f'Length of longest contiguous chain across all posibble shifting: {longest_chain}')
            print('')


        opt = menu_operation()

main()