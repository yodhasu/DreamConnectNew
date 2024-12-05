// Expose PIXI globally
window.PIXI = PIXI;

// Add a click listener to the button to initialize everything
document.getElementById('startButton').addEventListener('click', async () => {
    const app = new PIXI.Application({
        view: document.getElementById('canvas'),
        width: innerWidth,
        height: innerHeight,
        autoStart: true,
        resizeTo: window,
        transparent: true,
        clearBeforeRender: false,
        backgroundAlpha: 0
    });

    app.renderer.gl.clearColor(0, 0, 0, 0); // Fully transparent
    // Function to initialize and setup the socket
    const setupSocket = () => {
        const socket = io('http://127.0.0.1:9090');

        socket.on('connect', () => {
            console.log('Connected to Socket.IO server');
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from Socket.IO server');
            window.location.reload();
        });

        socket.on('model_action', async (data) => {
            const command = data.action.trim();
            console.log("Message from server:", command);

            // Stop previous actions and set neutral expression
            model.stopMotions();
            model.expression('neutral');
            model.motion('neutral');
            model.internalModel.motionManager.expressionManager.restoreExpression();

            // Set new expression
            await model.expression(command);
            await playAudio(); // Play audio after setting the expression

            console.log("Expression:", command);
        });

        socket.on('error', (error) => {
            console.error("Socket.IO Error:", error);
        });
    };

    // Function to play audio, only callable after user interaction
    const playAudio = async () => {
        const audioLink = 'http://127.0.0.1:9090/audio';
        try {
            await model.speak(audioLink, {
                volume: 2,
                crossOrigin: "anonymous",
                onFinish: () => { console.log("Voiceline is over"); },
                onError: (err) => { console.log("Error: " + err); }
            });
        } catch (err) {
            console.error("Error while trying to speak:", err);
        }
    };
    app.renderer.backgroundColor = 0x00000000; // Transparent black
    // Load the Live2D model
    const modeldir = "/model/March 7th/march 7th.model3.json";
    const model = await PIXI.live2d.Live2DModel.from(modeldir);
    // app.renderer.backgroundColor = null; // Or 0x00000000 for fully transparent
    
    // app.renderer.transparent = true;

    app.stage.addChild(model);
    // model.alpha = 1.0
    console.log("PIXI transparent:", app.renderer.transparent);
    console.log("Renderer backgroundColor:", app.renderer.backgroundColor);
    console.log("WebGL clearColor:", app.renderer.gl.getParameter(app.renderer.gl.COLOR_CLEAR_VALUE)); // Should print [0, 0, 0, 0]

    // Adjust model properties
    model.x = app.screen.width / 2;
    model.y = app.screen.height / 2;
    model.anchor.set(0.28, 0.47);
    model.scale.set(0.1, 0.1);
    model.position.set(window.innerWidth / 4, window.innerHeight / 2);
    model.focus(0, 0, true);

    // Call setupSocket to connect to server
    setupSocket();

    // Flag to control mouse movement detection
    let mouseMovementEnabled = false;

    // Pan functionality
    let isPanning = false;
    let panStartPosition = { x: 0, y: 0 };
    let stageStartPosition = { x: 0, y: 0 };

    const handleMouseDown = (event) => {
        isPanning = true;
        panStartPosition = { x: event.clientX, y: event.clientY };
        stageStartPosition = { x: app.stage.x, y: app.stage.y };
    };

    const handleMouseMove = (event) => {
        if (isPanning) {
            const dx = event.clientX - panStartPosition.x;
            const dy = event.clientY - panStartPosition.y;
            app.stage.x = stageStartPosition.x + dx;
            app.stage.y = stageStartPosition.y + dy;
        }
    };

    const handleMouseUp = () => {
        isPanning = false;
    };

    // Event listener for enabling mouse movement
    const enableMouseMovement = () => {
        mouseMovementEnabled = true;
        window.addEventListener('mousemove', handleMouseMove);
    };

    // Click event to enable mouse movement detection
    // window.addEventListener('click', () => {
    //     if (!mouseMovementEnabled) {
    //         enableMouseMovement(); // Enable mouse movement only after the first click
    //     }
    // });

    // Event listeners for panning
    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mouseup', handleMouseUp);

    // Optional: Scroll zoom function
    const handleScrollZoom = (event) => {
        event.preventDefault();
        const zoomFactor = 0.1;
        const newScale = app.stage.scale.x + (event.deltaY > 0 ? -zoomFactor : zoomFactor);
        app.stage.scale.set(newScale, newScale);
    };

    window.addEventListener('wheel', handleScrollZoom);

    // Cleanup on component unmount
    window.addEventListener('resize', () => {
        app.renderer.resize(window.innerWidth, window.innerHeight); // Adjust canvas size on window resize
    });

    // Cleanup on component unmount
    return () => {
        window.removeEventListener('wheel', handleScrollZoom);
        window.removeEventListener('click', enableMouseMovement);
        window.removeEventListener('mousedown', handleMouseDown);
        window.removeEventListener('mouseup', handleMouseUp);
        if (mouseMovementEnabled) {
            window.removeEventListener('mousemove', handleMouseMove);
        }
        if (app) app.destroy(true, { children: true, texture: true, baseTexture: true });
    };

});
