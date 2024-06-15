from args import args
from showcase import Showcase
from communicate import Client


def run():

    if len(args.url) == 1:
        url = args.url[0]
    else:
        url = args.url

    com_address = (args.com_host, args.com_port)

    if args.com_exec:
        exit(Client(com_address).com(str(" ").join(args.url).encode()))
    elif args.com_back:
        exit(Client(com_address).com_back())
    elif args.com_forward:
        exit(Client(com_address).com_forward())
    elif args.com_reload:
        exit(Client(com_address).com_reload())
    elif args.com_home:
        exit(Client(com_address).com_home())
    elif args.com_stop_load:
        exit(Client(com_address).com_stop_load())
    elif args.com_quit:
        exit(Client(com_address).com_quit())
    elif args.com_tab_change is not None:
        exit(Client(com_address).com_tab_change(args.com_tab_change))
    elif args.com_tab_close is not None:
        exit(Client(com_address).com_tab_close(args.com_tab_close))
    elif args.com_try:
        try:
            exit(Client(com_address).com_load(url, args.com_tab_index, args.com_tab_append))
        except ConnectionRefusedError:
            pass
    elif args.com_ping:
        exit(not Client(com_address).com_ping())

    if args.com or args.com_try:
        print(f"Serving Communicator at {com_address[0]}:{com_address[1]}")
    else:
        com_address = None

    showcase = Showcase(
        url or '',
        args.wg_url,
        args.ks_url,
        args.wg_back,
        args.ks_back,
        args.wg_forward,
        args.ks_forward,
        args.wg_refresh,
        args.ks_refresh,
        args.wg_home,
        args.ks_home,
        args.home_url,
        args.wg_stop,
        args.ks_stop,
        args.wg_tabs,
        args.wg_tabs_close,
        args.ks_tabs_close,
        args.wg_tabs_add,
        args.ks_tabs_add,
        args.tabs_default_url,
        args.tabs_default_label,
        args.tabs_dynamic_labels,
        args.tabs_keep_last,
        args.window_title,
        args.window_icon,
        args.window_maxsize,
        com_address,
    )

    showcase.exec()


if __name__ == "__main__":
    run()
