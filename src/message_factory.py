from struct import unpack

from formats import S, R, H, Y, L, V, W, K, J, h, A, F, E, C, X, D, U, P, Q, B, I, N, O


class MessageFactory:
    unpack_bin_format = {'A': '>HH6sQsI8sI', 'B': '>HH6sQ', 'C': '>HH6sQIQsI', 'D': '>HH6sQ', 'E': '>HH6sQIQ',
                         'F': '>HH6sQsI8sI4s', 'H': '>HH6s8sss4s', 'I': '>HH6sQQs8sIIIss', 'J': '>HH6s8sIIII',
                         'K': '>HH6s8sIsI', 'L': '>HH6s4s8ssss', 'N': 'HH6s8ss', 'O': 'HH6s8ssIIIQII',
                         'P': '>HH6sQsI8sIQ', 'Q': '>HH6sQ8sIQs', 'R': '>HH6s8sssIss2ssssssIs', 'S': '>HH6ss',
                         'U': '>HH6sQQII', 'V': '>HH6sQQQ', 'W': '>HH6ss', 'X': '>HH6sQI', 'Y': '>HH6s8ss',
                         'h': '>HH6s8sss'}
    unpack_message_format = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E,
                             'F': F, 'H': H, 'I': I, 'J': J,
                             'K': K, 'L': L, 'N': N, 'O': O, 'P': P, 'Q': Q,
                             'R': R, 'S': S, 'U': U, 'V': V, 'W': W,
                             'X': X, 'Y': Y, 'h': h}

    @staticmethod
    def create_message(message_type, data):
        try:
            unpacked_data = unpack(MessageFactory.unpack_bin_format[message_type], data)
            return MessageFactory.unpack_message_format[message_type](*unpacked_data)
        except:
            print(message_type)
