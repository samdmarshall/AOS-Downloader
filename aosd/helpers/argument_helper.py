

class argument_helper(object):
    
    @classmethod
    def parse(cls, arguments_str):
        arguments_str = str(arguments_str)
        arg_words = []
        input_split = arguments_str.split(' ')
        offset = 0
        counter = 0
        current_word = ''
        while counter < len(input_split):
            word = input_split[counter]
            current_word += word
            if len(current_word) == 0:
                offset += 1
            else:
                if offset >= 0:
                    curr = offset + len(word)
                    prev = curr - 1
                    if arguments_str[prev:curr] != '\\':
                        arg_words.append(current_word)
                        current_word = ''
                    else:
                        current_word += ' '
                    offset += len(word) + 1
            counter += 1
        return arg_words