# coding: utf-8
import sys
import time
import libtorrent


class Torrent(object):

    def __init__(self, base_path, target_file, tracker_list=None):
        self.base_path = base_path
        self.target_file = target_file
        self.tracker_list = tracker_list or [] + self._private_tracker_list

    @property
    def _private_tracker_list(self):
        return map(str.strip, '''
            udp://122.227.254.61:10050
        '''.split('\n')[1:-1])

    def hash(self):
        pass

    def create_torrent(self, torrent_path, creator=None, comment=None):
        fs = libtorrent.file_storage()
        libtorrent.add_files(fs, self.target_file)
        t = libtorrent.create_torrent(fs)
        for tracker in self.tracker_list:
            t.add_tracker(tracker, 0)
        t.set_creator(creator or 'libtorrent %s' % libtorrent.version)
        t.set_comment(comment or 'kanjian')
        libtorrent.set_piece_hashes(t, self.base_path)
        torrent = t.generate()
        f = open(torrent_path, "wb")
        f.write(libtorrent.bencode(torrent))
        f.close()

    @classmethod
    def seed(cls, torrent_path, save_path, seed_mode=True):
        ses = libtorrent.session()
        ses.listen_on(6881, 6891)
        h = ses.add_torrent({
            'ti': libtorrent.torrent_info(torrent_path),
            'save_path': save_path,
            'seed_mode': seed_mode,
        })
        while True:
            s = h.status()
            state_str = ['queued', 'checking', 'downloading metadata',
                         'downloading', 'finished', 'seeding',
                         'allocating', 'checking fastresume']

            print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
            sys.stdout.flush()
            time.sleep(1)
