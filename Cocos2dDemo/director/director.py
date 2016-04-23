import cocos

if __name__ == '__main__':
    cocos.director.director.init(
            # fullscreen    = True,
            resizable     = True,
            width         = 400,
            height        = 300,
            caption       = "Cocos Windows Title",
            autoscale     = True,
        )
    cocos.director.director.run(cocos.scene.Scene())
