from torrent import Torrent

# Create torrent
if __name__ == '__main__':
    t = Torrent('/data/', '/data/torrent-test/')
    t.create_torrent('/home/tcc/torrent/test.torrent', comment='test')
