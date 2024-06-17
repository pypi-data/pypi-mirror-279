import random

def create_symbols(text: list[str]):
    united_phrases = ' '.join(text)
    letter_set = set(united_phrases)
    list_of_letters = list(letter_set)

    return list_of_letters

def create_dictionary_of_keys(symbols):
    max_number = random.randint(150, 300)
    prime_numbers = []
    
    if not symbols:
        symbols = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']

    for i in range(2, max_number):
        z = 0
            
        for j in range(2, i):
            if i % j == 0:
                z = 1
                break

        if z == 0:
            prime_numbers.append(i)
        
    dictionary_of_keys = {"layer 0": {symbols[0]: random.choice(prime_numbers)}, "layer 1": {}}
    used_values = {list(dictionary_of_keys["layer 0"].values())[0]}  # Set to keep track of used values

    del symbols[0]
    
    layer = 1
    id_previous_layer = 0  # Its function is to select the upstream element that must be added two other elements
    counter = 0  # Its function is to ensure that only two elements are assigned to the upstream element.
    i = 1  # Its function is to ensure that an empty layer is not created

    for symbol in symbols:        
        random_number = random.choice(prime_numbers)
        value_1_upstream = list(dictionary_of_keys[f'layer {id_previous_layer}'].values())[id_previous_layer]

        new_value = value_1_upstream * random_number
        
        # Ensure new_value is unique
        while new_value in used_values:
            random_number = random.choice(prime_numbers)
            new_value = value_1_upstream * random_number

        dictionary_of_keys[f'layer {layer}'][symbol] = new_value
        used_values.add(new_value)

        if len(list(dictionary_of_keys[f'layer {layer}'].values())) == 2 ** layer:
            # A new layer is created
            
            if len(symbols) == i:  # Prevents an empty layer from being created
                break

            layer += 1
            id_previous_layer = 0
            dictionary_of_keys[f'layer {layer}'] = {}
        else: 
            # Checks if the upstream element needs to be changed
            
            if counter == 2:
                id_previous_layer += 1
                counter = 0

            else:
                counter += 1

        i += 1

    return dictionary_of_keys

def encode(text: list[str], dictionary_of_keys):
    encode_text = []
    
    for line in text:
        for i in range(len(dictionary_of_keys)):
            layer = dictionary_of_keys[f"layer {i}"]
                
            for j in range(len(layer)):
                symbol = list(layer.keys())[j]
                encode_symbol = str(list(layer.values())[j]) + ','

                line = line.replace(symbol, encode_symbol)

        encode_text.append(line)

    return encode_text

def decode(text: list[str], dictionary_of_keys):
    # reverse the dictionary
    inverted_dict = {}
    for layer, chars in dictionary_of_keys.items():
        for char, num in chars.items():
            inverted_dict[str(num)] = char

    decode_text = []

    for line in text:
        decode_line = []

        for word in line.split(', '):
            decode_word = []

            for number in word.split(','):
                decode_letter = inverted_dict.get(str(number.strip()), '')
                decode_word.append(decode_letter)
            
            decode_word_join = ''.join(decode_word)
            decode_line.append(decode_word_join)

        decode_line_join = ' '.join(decode_line)
        decode_text.append(decode_line_join)

    return decode_text

def test():
    cases = [
        {'text' : ['hello my name is kopo', 'hello kopo', 'can you give a onion kopo', 'of course i will do that'], 'symbols' : None}, # test if the program can work with lowercase letters
        {'text' : ['IOPOI PODI', 'DI'], 'symbols' : None}, # test if the program can work with capital letters
        {'text' : ['12 34 19', '98 09 12 13'], 'symbols' : None}, # test if the program can work with numbers
        {'text' : ['////?????? ####,,,,....======'], 'symbols' : None}, # test if the program can work with symbols
        {'text' : ['Ho mo lo 123-123-234-55', 'Po om pol #pom', '1 + 2 = 3'], 'symbols' : None} # test if the program can work with all mix
    ]
    result = []

    for text in cases:
        text['symbols'] = create_symbols(text=text['text'])

        dictionary_of_keys = create_dictionary_of_keys(text['symbols'])

        encode_text = encode(
            text=text['text'],
            dictionary_of_keys=dictionary_of_keys
        )

        decode_text = decode(
            text=encode_text,
            dictionary_of_keys=dictionary_of_keys
        )

        if text['text'] == decode_text:
            result.append(True)
        else:
            a = text['text']

            print(f'''
Expected text: {a}

Text received: {decode_text}
            ''')

            result.append(False)

    return result

if __name__ == '__main__':
    print(test())
