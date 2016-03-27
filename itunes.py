import sys
import itertools


try:
    pyobjc_path = '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC/'
    sys.path.append(pyobjc_path)
    from ScriptingBridge import SBApplication
    from Foundation import NSMutableIndexSet, NSURL
except ImportError:
    print 'Unable to find PyObjC at ' + pyobjc_path


class ITunes(object):
    def __init__(self):
        self.app = app = SBApplication.applicationWithBundleIdentifier_('com.apple.iTunes')
        self.app.setFixedIndexing_(True)
        self.source = first(app.sources(), lambda x: x.name() == 'Library')

    @property
    def playlists(self):
        return (Playlist(p) for p in self.source.userPlaylists())

    @property
    def tracks(self):
        "Return all music tracks."
        return self['Music'].tracks

    def __getitem__(self, name):
        playlist = first(self.source.userPlaylists(), lambda x: x.name() == name)
        return Playlist(playlist)


class Playlist(object):
    "Wrapper class for ITunesUserPlaylist"
    def __init__(self, playlist):
        self._playlist = playlist

    @property
    def name(self):
        return self._playlist.name()

    @property
    def tracks(self):
        return (Track(t) for t in self._playlist.tracks())


class Track(object):
    "Wrapper class for ITunesTrack"
    def __init__(self, track):
        self._track = track

    @property
    def title(self): return self._track.name()

    @property
    def artist(self): return self._track.artist()

    @property
    def rating(self): return self._track.rating()

    @property
    def genre(self): return self._track.genre()

    @property
    def stars(self):
        rating = self.rating
        if rating == 100:
            return 5
        elif rating >= 80:
            return 4
        elif rating >= 60:
            return 3
        elif rating >= 40:
            return 2
        elif rating >= 20:
            return 1
        else:
            return 0

    @property
    def path(self): return self._track.get().location().path()


def first(iterable, predicate):
    "Return the first element in `iterable` that matches `predicate`."
    try:
        return itertools.ifilter(predicate, iterable).next()
    except StopIteration:
        return None


if __name__ == '__main__':
    tunes = ITunes()
    for p in tunes.tracks:
        print t.title
        print t.artist
        print t.genre
        print t.stars
