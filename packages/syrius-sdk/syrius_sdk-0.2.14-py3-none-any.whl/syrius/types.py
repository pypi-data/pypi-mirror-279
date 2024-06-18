from typing import Union

from syrius.commands import ArrayFilterByCommand, ArrayKeyValueCommand, ArrayLengthCommand, \
    ArrayOfKeyValueToArrayCommand, ArrayReduceByKeyCommand, ArraysMergeByKeyCommand, CurrencyFormatterCommand, \
    FileTextExtractCommand, FileUploadCommand, GrtCommand, IfCommand, OpenAICompletionCommand, \
    PdfHighlighterCommand, SectionSplitterCommand, SectionRemoverCommand, SentencesSplitterCommand, TemplateCommand, \
    UnstructuredCommand
from syrius.loops.ForCommand import ForCommand

commands_union = ArrayFilterByCommand | ArrayKeyValueCommand | ArrayLengthCommand | ArrayOfKeyValueToArrayCommand | ArrayReduceByKeyCommand | ArraysMergeByKeyCommand | CurrencyFormatterCommand | FileTextExtractCommand | FileUploadCommand | ForCommand | GrtCommand | IfCommand | OpenAICompletionCommand | PdfHighlighterCommand | SectionSplitterCommand | SectionRemoverCommand | SentencesSplitterCommand | TemplateCommand | UnstructuredCommand
