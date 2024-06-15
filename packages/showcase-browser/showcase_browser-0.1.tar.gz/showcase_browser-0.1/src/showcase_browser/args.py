from argparse import ArgumentParser
from __init__ import __version__


parser = ArgumentParser(
    prog="showcase",
    description="This minimalistic program turns any website or other document into a stand-alone application.",
    epilog=f"ShowCase Browser v{__version__} (https://github.com/srccircumflex/ShowCase-Browser)",
)

parser.add_argument(
    "url",
    action="store",
    default=None,
    help="The content url. If several are passed, the tab widget is "
         "automatically added and makes `--wg-tabs' redundant.",
    nargs="*",
    type=str
)

basic_wg_group = parser.add_argument_group(
    "Basic Widgets",
    description="Add optional basic widgets.",
)
basic_ks_group = parser.add_argument_group(
    "Basic Key Sequences",
    description="Add and define optional basic key sequences. "
                "The argument is passed as a string to a PyQt6.QKeySequence. "
                "Visit https://doc.qt.io/qt-6/qkeysequence.html#details for more information.",
)
home_group = parser.add_argument_group(
    "Home",
    "Add and define the Home functions.",
)
taps_group = parser.add_argument_group(
    "Tabs",
    description="Add and define the Tabs functions."
)
window_group = parser.add_argument_group(
    "Window",
    description="Window parameters"
)
com_group = parser.add_argument_group(
    "Communicator",
    description="Create a communicator for showcase."
)
com_addr_group = parser.add_argument_group(
    "Communicator Address",
    description="Define the communicator address. "
                "For the transmission or the server. "
                "The default is `127.0.0.3:51001'."
)
com_url_group = parser.add_argument_group(
    "Communicator Url Handle",
    description=""
)
com_ex_group = parser.add_argument_group(
    "Communicate Commands",
    description="Send the command and exit."
)
com_ex_group = com_ex_group.add_mutually_exclusive_group()


try:
    basic_wg_group.add_argument(
        "--wg-url",
        action="store_true",
        default=False,
        help="Add the url entry.",
    )
    basic_wg_group.add_argument(
        "--wg-back",
        action="store_true",
        default=False,
        help="Add the back button.",
    )
    basic_wg_group.add_argument(
        "--wg-forward",
        action="store_true",
        default=False,
        help="Add the forward button.",
    )
    basic_wg_group.add_argument(
        "--wg-refresh",
        action="store_true",
        default=False,
        help="Add the refresh button.",
    )
    basic_wg_group.add_argument(
        "--wg-stop",
        action="store_true",
        default=False,
        help="Add the stop button.",
    )
except Exception:
    raise

try:
    basic_ks_group.add_argument(
        "--ks-url",
        action="store",
        help="Add a key sequence to put the focus on the url widget "
             "(e.g. `Ctrl+L').",
        metavar="<key sequence>",
    )
    basic_ks_group.add_argument(
        "--ks-back",
        action="store",
        help="Add a key sequence to trigger the back function "
             "(e.g. `Ctrl+Backspace').",
        metavar="<key sequence>",
    )
    basic_ks_group.add_argument(
        "--ks-forward",
        action="store",
        help="Add a key sequence to trigger the forward function "
             "(e.g. `Ctrl+Shift+Backspace').",
        metavar="<key sequence>",
    )
    basic_ks_group.add_argument(
        "--ks-refresh",
        action="store",
        help="Add a key sequence to trigger the refresh function "
             "(e.g. `Ctrl+R').",
        metavar="<key sequence>",
    )

    basic_ks_group.add_argument(
        "--ks-stop",
        action="store",
        help="Add a key sequence to trigger the stop load function "
             "(e.g. `Ctrl+X').",
        metavar="<key sequence>",
    )
except Exception:
    raise

try:
    home_group.add_argument(
        "--wg-home",
        action="store_true",
        default=False,
        help="Add the home button.",
    )
    home_group.add_argument(
        "--ks-home",
        action="store",
        help="Add a key sequence to trigger the home function "
             "(e.g. `Ctrl+H').",
        metavar="<key sequence>",
    )
    home_group.add_argument(
        "--home-url",
        action="store",
        help="Define the home url. [*] required for the upper functions",
        metavar="<url>",
    )
except Exception:
    raise

try:
    taps_group.add_argument(
        "--wg-tabs",
        action="store_true",
        default=False,
        help="Add the tabs widget.",
    )
    taps_group.add_argument(
        "--wg-tabs-close",
        action="store_true",
        default=False,
        help="Add the close button for each tab.",
    )
    taps_group.add_argument(
        "--ks-tabs-close",
        action="store",
        help="Add a key sequence to trigger the tab close function "
             "(e.g. `Ctrl+-').",
        metavar="<key sequence>",
    )
    taps_group.add_argument(
        "--wg-tabs-add",
        action="store_true",
        default=False,
        help="Add the add tab button.",
    )
    taps_group.add_argument(
        "--ks-tabs-add",
        action="store",
        help="Add a key sequence to trigger the tab add function "
             "(e.g. `Ctrl++').",
        metavar="<key sequence>",
    )
    taps_group.add_argument(
        "--tabs-default-url",
        action="store",
        help="Add a key sequence to trigger the tab close function "
             "(e.g. `Ctrl+-').",
        type=str
    )
    taps_group.add_argument(
        "--tabs-default-label",
        action="store",
        help="Define a default tab label.",
        type=str
    )
    taps_group.add_argument(
        "--tabs-dynamic-labels",
        action="store_true",
        default=False,
        help="Tablabels are obtained from the loaded pages.",
    )
    taps_group.add_argument(
        "--tabs-keep-last",
        action="store_true",
        default=False,
        help="It is not possible to close the last tab.",
    )
except Exception:
    raise

try:
    window_group.add_argument(
        "--window-title",
        action="store",
        help="Define the window title.",
        type=str
    )
    window_group.add_argument(
        "--window-icon",
        action="store",
        help="Define the path to the window icon.",
        type=str
    )
    window_group.add_argument(
        "--window-maxsize",
        action="store_true",
        default=False,
        help="Maximize the window at startup.",
    )
except Exception:
    raise

try:
    com_group.add_argument(
        "--com",
        action="store_true",
        default=False,
    )

    com_addr_group.add_argument(
        "--com-host",
        action="store",
        default="127.0.0.3",
        metavar="xxx.xxx.xxx.xxx",
    )
    com_addr_group.add_argument(
        "--com-port",
        action="store",
        default=51_001,
        metavar="port-number",
        type=int,
    )

    com_url_group.add_argument(
        "--com-try",
        action="store_true",
        default=False,
        help="Try to transfer the url to a communicator, "
             "start a showcase with the url and a communicator "
             "if not possible. "
             "With this flag only one url is allowed.",
    )
    com_url_group.add_argument(
        "--com-tab-append",
        action="store_true",
        default=False,
        help="If `--com-try' is successful and the tab widget is active, "
             "add the url as a new tab.",
    )
    com_url_group.add_argument(
        "--com-tab-index",
        action="store",
        default=None,
        help="If `--com-try' is successful and the tab widget is active, "
             "overwrite the url of tab `n'.",
        metavar="n",
        type=int
    )

    com_ex_group.add_argument(
        "--com-back",
        action="store_true",
        default=False,
        help="Trigger the back function.",
    )
    com_ex_group.add_argument(
        "--com-forward",
        action="store_true",
        default=False,
        help="Trigger the forward function.",
    )
    com_ex_group.add_argument(
        "--com-reload",
        action="store_true",
        default=False,
        help="Trigger the reload function.",
    )
    com_ex_group.add_argument(
        "--com-home",
        action="store_true",
        default=False,
        help="Trigger the home function.",
    )
    com_ex_group.add_argument(
        "--com-stop-load",
        action="store_true",
        default=False,
        help="Trigger the stop load function.",
    )
    com_ex_group.add_argument(
        "--com-quit",
        action="store_true",
        default=False,
        help="Trigger the quit function.",
    )
    com_ex_group.add_argument(
        "--com-tab-change",
        action="store",
        default=None,
        help="Change the focus to tab `n'.",
        metavar="n",
        type=int
    )
    com_ex_group.add_argument(
        "--com-tab-close",
        action="store",
        default=None,
        help="Close the tab on index `n'. "
             "Use -1 to close the focused tab.",
        metavar="n",
        type=int
    )
    com_ex_group.add_argument(
        "--com-exec",
        action="store_true",
        default=False,
        help="Execute the string that is passed at the position of the "
             "url with the python exec function.",
    )
    com_ex_group.add_argument(
        "--com-ping",
        action="store_true",
        default=False,
        help="Try to connect with the communicator. "
             "The program exits with code 0 if successful.",
    )

except Exception:
    raise

args = parser.parse_args()
