from proposition import PropositionTypes
from true_sentence import TrueSentence
from action import Action
from arg_types import ArgTypes
from arg import Arg


def getActions():
    """
    Hardcoded actions for the Blocks World.
    """

    pickBlock = Action(
        'pick',
        ['block'],
        [
            TrueSentence(PropositionTypes.ONTABLE, [Arg(ArgTypes.VARIABLE, 'block', False)], False),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'block', False)], False),
            TrueSentence(PropositionTypes.EMPTY, [], False)
        ],
        [
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'block', False)], False),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'block', False)], True),
            TrueSentence(PropositionTypes.ONTABLE, [Arg(ArgTypes.VARIABLE, 'block', False)], True),
            TrueSentence(PropositionTypes.EMPTY, [], True)
        ]
    )

    unstackBlockAFromTopOfBlockB = Action(
        'unstack',
        ['blocka', 'blockb'],
        [
            TrueSentence(
                PropositionTypes.ON,
                [
                    Arg(ArgTypes.VARIABLE, 'blocka', False),
                    Arg(ArgTypes.VARIABLE, 'blockb', False)
                ],
                False
            ),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blocka', False)], False),
            TrueSentence(PropositionTypes.EMPTY, [], False)
        ],
        [
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'blocka', False)], False),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blockb', False)], False),
            TrueSentence(
                PropositionTypes.ON, [
                    Arg(ArgTypes.VARIABLE, 'blocka', False),
                    Arg(ArgTypes.VARIABLE, 'blockb', False)
                ],
                True
            ),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blocka', False)], True),
            TrueSentence(PropositionTypes.EMPTY, [], True)
        ]
    )

    releaseBlock = Action(
        'release',
        ['block'],
        [
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'block', False)], False)
        ],
        [
            TrueSentence(PropositionTypes.ONTABLE, [Arg(ArgTypes.VARIABLE, 'block', False)], False),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'block', False)], False),
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'block', False)], True),
            TrueSentence(PropositionTypes.EMPTY, [], False)
        ]
    )

    stackBlockAOnTopOfBlockB = Action(
        'stack',
        ['blocka', 'blockb'],
        [
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blockb', False)], False),
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'blocka', False)], False)
        ],
        [
            TrueSentence(
                PropositionTypes.ON,
                [
                    Arg(ArgTypes.VARIABLE, 'blocka', False),
                    Arg(ArgTypes.VARIABLE, 'blockb', False)
                ],
                False
            ),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blocka', False)], False),
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'blocka', False)], True),
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blockb', False)], True),
            TrueSentence(PropositionTypes.EMPTY, [], False)
        ]
    )

    return [
        pickBlock,
        unstackBlockAFromTopOfBlockB,
        releaseBlock,
        stackBlockAOnTopOfBlockB
    ]
