###########################################################
#
# Copyright (c) 2013, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#


__all__ = ['VideoWdg']

from tactic.ui.common import BaseRefreshWdg
from pyasm.web import Video, HtmlElement, DivWdg



class VideoWdg(BaseRefreshWdg):

    ARGS_KEYS = {
        "sources": {
            'description': 'List of URLs representing the sources for the videos, separate by "|"',
            'type': 'TextAreaWdg',
            'category': 'Options',
        },
        'width': 'The width to display the video',
        'height': 'The height to display the video',
        'poster': 'Link to an image for the poster representing the video',
    }

    def init(my):
        my.video = Video()



    def get_video(my):
        return my.video

    def get_display(my):

        top = my.top

        sources = my.kwargs.get("sources")
        if sources and isinstance(sources, basestring):
            sources = sources.split("|")

        source_types = my.kwargs.get("source_types")
        if not source_types:
            source_types = []


        poster = my.kwargs.get("poster")
        width = my.kwargs.get("width")
        height = my.kwargs.get("height")
        preload = my.kwargs.get("preload")
        controls = my.kwargs.get("controls")
        autoplay = my.kwargs.get("autoplay")

        video = my.video
        top.add(video)

        my.video_id = my.kwargs.get("video_id")
        if not my.video_id:
            my.video_id = video.set_unique_id()
        else:
            video.set_attr("id", my.video_id)


        top.add_behavior( {
            'type': 'load',
            'cbjs_action': my.get_onload_js()
        } )

        top.add_behavior( {
            'type': 'load',
            'video_id': my.video_id,
            'cbjs_action': '''
            spt.video.init_video(bvr.video_id);
            '''
        } )


        if width:
            video.add_attr("width", width)
        if height:
            video.add_attr("height", height)

        if poster:
            video.add_attr("poster", poster)

        if preload == None:
            preload = "auto"
        elif preload == False:
            preload = "none"


        autoplay = "false"

        video.add_attr("preload", preload)

        #video.add_attr("autoplay", autoplay)
        if controls:
            video.add_attr("controls", controls)


        for i, src in enumerate(sources):

            source = HtmlElement(type="source")
            source.add_attr("src", src)

            if len(source_types) > i:
                source_type = source_types[i]
                source.add_attr("type", source_type)

            video.add(source)

        #print top.get_buffer_display()
        return top



    def get_onload_js(my):
        return '''

spt.video = {}

spt.video.loaded = false;
spt.video.player = null;

spt.video.players = {};


spt.video.get_player_el = function(el) {
    var video = el.getElement("video");
    return video;
}

spt.video.get_player = function(el) {
    var video = el.getElement("video");
    return video;
}

spt.video.init_video = function(video_id) {

    spt.video.loaded = true;
    spt.video.player = $(video_id);
    spt.video.players[video_id] = spt.video.player;
}
        '''

















class VideoWdgX(BaseRefreshWdg):

    ARGS_KEYS = {
        "sources": {
            'description': 'List of URLs representing the sources for the videos, separate by "|"',
            'type': 'TextAreaWdg',
            'category': 'Options',
        },
        'width': 'The width to display the video',
        'height': 'The height to display the video',
        'poster': 'Link to an image for the poster representing the video',
    }

    def init(my):
        my.video = Video()

        my.index = my.kwargs.get('index')

    def get_video(my):
        return my.video

    def get_display(my):

        top = my.top

        sources = my.kwargs.get("sources")
        if sources and isinstance(sources, basestring):
            sources = sources.split("|")

        source_types = my.kwargs.get("source_types")
        if not source_types:
            source_types = []


        poster = my.kwargs.get("poster")
        width = my.kwargs.get("width")
        height = my.kwargs.get("height")
        preload = my.kwargs.get("preload")
        controls = my.kwargs.get("controls")
        autoplay = my.kwargs.get("autoplay")

        use_videojs = my.kwargs.get("use_videojs")
        if not use_videojs:
            use_videojs = True


        is_test = my.kwargs.get("is_test")
        is_test = False
        if is_test in [True, 'true']:
            poster = "http://video-js.zencoder.com/oceans-clip.png"
            sources = ["http://video-js.zencoder.com/oceans-clip.mp4"]
            sources = ["http://video-js.zencoder.com/oceans-clip.mp4"]
            sources = ["http://techslides.com/demos/sample-videos/small.ogv"]


        video = my.video
        video.add_class("video-js")
        video.add_class("vjs-default-skin")
        top.add(video)

        my.video_id = my.kwargs.get("video_id")
        if not my.video_id:
            my.video_id = video.set_unique_id()
        else:
            video.set_attr("id", my.video_id)

        # FIXME: this has refereneces to the Gallery ....!
        if my.index == 0: 
            overlay = DivWdg()
            overlay.add_class('video_overlay')
            overlay.add_styles('background: transparent; z-index: 300; position: fixed; top: 38%; left: 12%;\
                margin-left: auto; margin-right: auto; width: 75%; height: 45%' )

           
            overlay.add_behavior({'type':'click_up',
                'cbjs_action': '''
                var overlay = bvr.src_el;
                
                var idx = spt.gallery.index;
                var video_id = spt.gallery.videos[idx];
                
                if (!video_id) return;

                var player = videojs(video_id, {"nativeControlsForTouch": false});
                if (player.paused()) {
                    player.play();
                    //console.log("play " + video_id)
                }
                else 
                    player.pause();
                '''
                })


            top.add(overlay) 



        top.add_behavior( {
            'type': 'load',
            'cbjs_action': my.get_onload_js()
        } )

        top.add_behavior( {
            'type': 'load',
            'index' : my.index,
            'video_id': my.video_id,
            'use_videojs': use_videojs,
            'cbjs_action': '''
            if (!bvr.index) bvr.index = 0;

            var video_id = bvr.video_id;


            if (bvr.use_videojs) {
                spt.video.init_videojs(video_id);
            }
            else {
                spt.video.init_video(video_id);
            }

            if (spt.gallery) {
                
                spt.gallery.videos[bvr.index] = video_id;

                if (!spt.gallery.portrait) {
                    var overlay = bvr.src_el.getElement('.video_overlay');
                    if (overlay)
                        overlay.setStyles({'top': '4%', 'left': '5%', 
                            'width': '90%', 'height':'87%'});
                }
            }
            
            
            '''
        } )
        #video.add_attr("data-setup", "{}")




        if width:
            video.add_attr("width", width)
        if height:
            video.add_attr("height", height)

        if poster:
            video.add_attr("poster", poster)

        if preload == None:
            preload = "none"

        if controls == None:
            controls = True

        autoplay = False

        # videojs uses a json data structre
        if use_videojs not in [False, 'false']:
            data = {
                    'preload': preload,
                    'controls': controls,
                    'autoplay': autoplay
            }

            from pyasm.common import jsondumps
            data_str = jsondumps(data)
            video.add_attr("data-setup", data_str)
        else:
            video.add_attr("preload", preload)
            video.add_attr("autoplay", autoplay)
            video.add_attr("controls", controls)



        for i, src in enumerate(sources):

            source = HtmlElement(type="source")
            source.add_attr("src", src)

            if len(source_types) > i:
                source_type = source_types[i]
                source.add_attr("type", source_type)

            video.add(source)

        #print top.get_buffer_display()
        return top



    def get_onload_js(my):
        return '''

spt.video = {}

spt.video.loaded = false;
spt.video.player = null;

spt.video.players = {};



spt.video.get_player_el = function(el) {
    var video = el.getElement(".video-js").getElement("video");
    return video;
}


spt.video.get_player = function(el) {
    var video = el.getElement(".video-js");
    var video_id = video.getAttribute("id");
    return spt.video.players[video_id];

}

spt.video.init_video = function(video_id, events) {

    if (spt.video.loaded) {
        spt.video._add_events(this, events);
    }
    else {
        spt.video.loaded = true;
        spt.video._add_events(this, events);

        spt.video.player = $(video_id);
        spt.video.players[video_id] = spt.video.player;
    }

}


spt.video.init_videojs = function(video_id, events) {

    if (spt.video.loaded) {
        var player = videojs(video_id, {"nativeControlsForTouch": false}, function() {
            spt.video._add_events(this, events);
        } )
    }
    else {

        spt.dom.load_js(["video/video.js"], function() {
            var player = videojs(
                    video_id,
                    {"nativeControlsForTouch": false},
                    function() {
                        spt.video.loaded = true;
                        spt.video._add_events(this, events);
                    }
            );
            spt.video.player = player;
            spt.video.players[video_id] = player;
        } )
    }

}


spt.video._add_events = function(player, events) {
    return;
}


        '''
