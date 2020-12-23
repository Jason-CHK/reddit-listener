import re

from praw.reddit import Submission as rs


class Submission(object):
    def __init__(self, sub: rs):
        self.title = sub.title.strip()
        self.flair = sub.link_flair_text
        self.type = 'unknown'
        self.tag = ''
        self.location = ''
        self.having = ''
        self.wanting = ''

        sections = [('[' + x).strip() for x in self.title.split('[') if x.strip()]

        if not sections:
            print(f'!!! ERROR: title is empty')
            return
        if len(sections) == 2 or len(sections) > 3:
            print(f'### WARNING: title has irregular sections: {self.title}')

        if len(sections) <= 2:
            self.extract_non_personal()

        if len(sections) >= 3:
            self.extract_personal(sections)

    def extract_non_personal(self):
        self.type = 'non-personal'
        match = re.fullmatch(r'\[(.+?)].*', self.title)
        if match:
            self.tag = match.group(1)
        else:
            print(f'### WARNING: non-personal title does not have valid tag: {self.title}')

    def extract_personal(self, sections: [str]):
        self.type = 'personal'

        match = re.fullmatch(r'\[(.+?)]', sections[0])
        if match:
            self.location = match.group(1)
        else:
            print(f'### WARNING: title does not have valid location: {self.title}')

        for section in sections[1:]:
            if section.startswith('[H]'):
                self.having = section[3:].strip()
            elif section.startswith('[W]'):
                self.wanting = section[3:].strip()
            else:
                print(f'### WARNING: unrecognized section: {section}, title: {self.title}')

    def __str__(self):
        header = f'title: {self.title}'
        if self.flair:
            header += f'\n  flair: {self.flair}'
        if self.type == 'non-personal':
            return header + f'\n  tag: {self.tag}'
        if self.type == 'personal':
            return header + f'\n  location: {self.location}' \
                            f'\n  having: {self.having}' \
                            f'\n  wanting: {self.wanting}'
        return header + f'\n  type: {self.type}'


if __name__ == '__main__':
    # Some tests.
    print(Submission(''))
    print(Submission('Space65 CyberVoyager Pink or White LED Badge'))
    print(Submission('[US-MD][H] PayPal [W] Space65 CyberVoyager Pink or White LED Badge'))
    print(Submission('[US-MD] [H] PayPal [W] Space65 CyberVoyager Pink or White LED Badge'))
    print(Submission('[US-MD] [H] PayPal [W] Space65 CyberVoyager Pink or White LED Badge [extra] text'))
