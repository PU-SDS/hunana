class SequenceFileNotFound(Exception):
    def __init__(self, seq_path: str):
        """
            Error raised when the FASTA file path is invalid, or the file is not found.
            
            :param seq_path: The path to the FASTA file.
            :type seq_path: str 
        """

        msg = f'\nThe FASTA file was not found at the following location:\n\t{seq_path}\nAdvice: \n\tPlease check ' \
              f'whether the path is valid, or contains any errors.'

        super(SequenceFileNotFound, self).__init__(msg)


class HeaderDecodeError(Exception):
    def __init__(self, header_format: str):
        """
            Error raised when the correct regex pattern could not be generated.

            :param header_format: The format of the FASTA header.
            :type header_format: str
        """

        msg = f'\nFailed to generate correct regex expression using the header format:\n\t{header_format}\nAdvice:\n\t' \
              f'Make sure the header format you provided accurately reflects the format of all the FASTA headers in ' \
              f'your FASTA file.'

        super(HeaderDecodeError, self).__init__(msg)


class SequenceLengthError(Exception):
    def __init__(self, groups_dict: dict):
        """
            Error raised when not all sequences in the slignment are of equal length.

            :param groups_dict: A dictionary containing sequences grouped by sequence length.
            :type groups_dict: dict
        """

        msg = '\nThe FASTA sequences provided does not appear to be aligned and are of various lengths.\n'

        error_data = []

        for length, sequences in groups_dict.items():
            headers = [sequence.description for sequence in sequences]
            headers_string = '\n\t'.join(headers)

            error_data.append(
                '\nLength: {length}\n\t{seqs}'.format(length=length, seqs=headers_string)
            )

        # Yes, this kind of string concatenation is bad, but it's a single time thing and doesn't cost much
        super(SequenceLengthError, self).__init__(msg + '\n'.join(error_data))


class NoSequencesProvided(Exception):
    def __init__(self):
        """
            Error raised when no sequences are provided by the user.
        """

        msg = 'No sequences are provided. Please make sure your FASTA file is not empty, or invalid.'

        super(NoSequencesProvided, self).__init__(msg)


class InvalidKmerLength(Exception):
    def __init__(self, seq_len: int, kmer_len: int):
        """
            Error raised when the kmer length is bigger than, or equal to the sequence length.

            :param seq_len: The length of the sequences provided by the user.
            :param kmer_len: The length of the kmers that user wants to generate.

            :type seq_len: int
            :type kmer_len: int
        """

        msg = f'The kmer length is bigger than, or equal to the length of the sequenced provided.\n\tKMER LENGTH: ' \
              f'{kmer_len}\n\tSEQUENCE LENGTH: {seq_len}'

        super(InvalidKmerLength, self).__init__(msg)
