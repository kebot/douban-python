import atom
import gdata

DOUBAN_NAMESPACE = 'http://www.douban.com/xmlns/'

def _t(v):
    if v is not None:
        return str(v)

def _decode(v):
    if v is not None:
        if isinstance(v, unicode) == False:
            return v.decode('utf-8')
        return v

class Location(atom.AtomBase):
    _tag = 'location'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    
    def __init__(self, loc=None, **kwargs):
        atom.AtomBase.__init__(self, text=loc, **kwargs)


class Uid(atom.AtomBase):
    _tag = 'uid'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    
    def __init__(self, loc=None, **kwargs):
        atom.AtomBase.__init__(self, text=loc, **kwargs)

class Rating(atom.AtomBase):
    """As gdata.py has not defined this element, we do this here.
    
    Should be removed when gdata.py includes the definition.

    """
    _tag = 'rating'
    _namespace = gdata.GDATA_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['average'] = 'average'
    _attributes['min'] = 'min'
    _attributes['max'] = 'max'
    _attributes['numRaters'] = 'numRaters'
    _attributes['value'] = 'value'

    def __init__(self, value=None, average=None, 
            min=1, max=5, numRaters=1, **kwargs):
        atom.AtomBase.__init__(self, **kwargs)
        self.value = _t(value)
        self.average = _t(average)
        self.min = _t(min)
        self.max = _t(max)
        self.numRaters = _t(numRaters)


class Attribute(atom.AtomBase):
    _tag = 'attribute'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['name'] = 'name'
    _attributes['index'] = 'index'
    _attributes['lang'] = 'lang'

    def __init__(self, name=None, value=None, index=None, lang=None, **kwargs):
        atom.AtomBase.__init__(self, text=value, **kwargs)
        self.name = name
        self.index = _t(index)
        self.lang = lang


class Tag(atom.AtomBase):
    _tag = 'tag'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    _attributes['count'] = 'count'
    _attributes['name'] = 'name'
    
    def __init__(self, name=None, count=None, **kwargs):
        atom.AtomBase.__init__(self, **kwargs)
        self.name = name
        self.count = _t(count)


class Status(atom.AtomBase):
    _tag = 'status'
    _namespace = DOUBAN_NAMESPACE
    _children = atom.AtomBase._children.copy()
    _attributes = atom.AtomBase._attributes.copy()
    
    def __init__(self, status=None, **kwargs):
        atom.AtomBase.__init__(self, text=status, **kwargs)


class Count(atom.AtomBase):
    _tag = 'count'
    _namespace = DOUBAN_NAMESPACE
    
    def __init__(self, count=None, **kwargs):
        atom.AtomBase.__init__(self, text=count, **kwargs)

def CreateClassFromXMLString(target_class, xml_string):
    return atom.CreateClassFromXMLString(target_class,
            xml_string.decode('utf8'), 'utf8')


class PeopleEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}location' % (DOUBAN_NAMESPACE)] = ('location', Location)
    _children['{%s}uid' % (DOUBAN_NAMESPACE)] = ('uid', Uid)

    def __init__(self, location=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.location = location

def PeopleEntryFromString(xml_string):
    return CreateClassFromXMLString(PeopleEntry, xml_string)


class PeopleFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [PeopleEntry])

def PeopleFeedFromString(xml_string):
    return CreateClassFromXMLString(PeopleFeed, xml_string)


class SubjectEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}rating' % (gdata.GDATA_NAMESPACE)] = ('rating', Rating)
    _children['{%s}attribute' % (DOUBAN_NAMESPACE)] = ('attribute', [Attribute])
    _children['{%s}tag' % (DOUBAN_NAMESPACE)] = ('tag', [Tag])

    def __init__(self, rating=None, attribute=None, tag=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.rating = rating
        self.attribute = attribute or []
        self.tag = tag or []


class Subject(SubjectEntry):
    """In some places we use <db:subject> to represent a subject entry."""
    _tag = 'subject'
    _namespace = DOUBAN_NAMESPACE
 
    def GetCollectionLink(self):
        for a_link in self.link:
            if a_link.rel == 'collection':
		return a_link	
 
class BookEntry(SubjectEntry):
    pass

def BookEntryFromString(xml_string):
    return CreateClassFromXMLString(BookEntry, xml_string)


class BookFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [BookEntry])

def BookFeedFromString(xml_string):
    return CreateClassFromXMLString(BookFeed, xml_string)


class MovieEntry(SubjectEntry):
    pass

def MovieEntryFromString(xml_string):
    return CreateClassFromXMLString(MovieEntry, xml_string)


class MovieFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [MovieEntry])

def MovieFeedFromString(xml_string):
    return CreateClassFromXMLString(MovieFeed, xml_string)


class MusicEntry(SubjectEntry):
    pass

def MusicEntryFromString(xml_string):
    return CreateClassFromXMLString(MusicEntry, xml_string)


class MusicFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [MusicEntry])

def MusicFeedFromString(xml_string):
    return CreateClassFromXMLString(MusicFeed, xml_string)


class ReviewEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}subject' % (DOUBAN_NAMESPACE)] = ('subject', Subject)
    _children['{%s}rating' % (gdata.GDATA_NAMESPACE)] = ('rating', Rating)

    def __init__(self, subject=None, rating=None, **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.subject = subject
        self.rating = rating

def ReviewEntryFromString(xml_string):
    return CreateClassFromXMLString(ReviewEntry, xml_string)


class ReviewFeed(gdata.GDataFeed):
    _tag = gdata.GDataFeed._tag
    _namespace = gdata.GDataFeed._namespace
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [ReviewEntry])

def ReviewFeedFromString(xml_string):
    return CreateClassFromXMLString(ReviewFeed, xml_string)


class CollectionEntry(gdata.GDataEntry):
    _tag = gdata.GDataEntry._tag
    _namespace = gdata.GDataEntry._namespace
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}status' % (DOUBAN_NAMESPACE)] = ('status', Status)
    _children['{%s}subject' % (DOUBAN_NAMESPACE)] = ('subject', Subject)
    _children['{%s}tag' % (DOUBAN_NAMESPACE)] = ('tags', [Tag])
    _children['{%s}rating' % (gdata.GDATA_NAMESPACE)] = ('rating', Rating)

    def __init__(self, status=None, subject=None, tag=None, rating=None,
            **kwargs):
        gdata.GDataEntry.__init__(self, **kwargs)
        self.status = status
        self.subject = subject
        self.tags = tag or []
        self.rating = rating

def CollectionEntryFromString(xml_string):
    return CreateClassFromXMLString(CollectionEntry, xml_string)

class CollectionFeed(gdata.GDataFeed):
    _children = gdata.GDataFeed._children.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [CollectionEntry])

def CollectionFeedFromString(xml_string):
    return CreateClassFromXMLString(CollectionFeed, xml_string)


class TagEntry(gdata.GDataEntry):
    _children = gdata.GDataEntry._children.copy()
    _children['{%s}count' % (DOUBAN_NAMESPACE)] = ('count', Count)
    def __init__(self, count=None, **kwargs):
        
        gdata.GDataEntry.__init__(self, **kwargs)
        self.count = count

class TagFeed(gdata.GDataFeed):
    _children = gdata.GDataFeed._children.copy()
    _children['{%s}entry' % (atom.ATOM_NAMESPACE)] = ('entry', [TagEntry])

def TagFeedFromString(xml_string):
    return CreateClassFromXMLString(TagFeed, xml_string)
