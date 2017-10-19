import yts_torrent_downloader as yts_ag
import argparse as ap

parser = ap.ArgumentParser()

parser.add_argument('movie', type = str, help = 'Enter a movie!!')
parser.add_argument('--info', action = 'store_true', help = 'To get info about the movie.')
parser.add_argument('--torrent', action = 'store_true', help = "To download torrent.")
parser.add_argument('--loc', type = str, action = 'store', dest = 'l', help = "Pass the saving location. Defaults to this folder.")

args = parser.parse_args()

if args.info and not args.torrent:
    yts_ag.movie_info(args.movie)

elif not args.info and args.torrent:
    if args.l:
        yts_ag.download_torrent(args.movie, args.l)
    else:
        yts_ag.download_torrent(args.movie)

elif args.info and args.torrent:
    yts_ag.movie_info(args.movie)

    if args.l:
        yts_ag.download_torrent(args.movie, args.l)
    else:
        yts_ag.download_torrent(args.movie)
