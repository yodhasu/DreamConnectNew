import { useEffect } from 'react';
// import { Live2DModel } from 'pixi-live2d-display-lipsyncpatch';
// or import { Live2DModel } from 'pixi-live2d-display-lipsyncpatch'; // i didn't test this
import * as PIXI from 'pixi.js';
import { Renderer } from '@pixi/core';
import { InteractionManager } from '@pixi/interaction';
import { Live2DModel, MotionPriority } from 'pixi-live2d-display';
import { io } from 'socket.io-client'; // Import socket.io-client
// window.EventEmitter = EventEmitter;
// PIXI.utils.EventEmitter

Renderer.registerPlugin('interaction', InteractionManager);
Live2DModel.registerTicker(PIXI.Ticker);
function App() {
  useEffect(() => {
    // Initialize PIXI Application
    const app = new PIXI.Application({
      view: document.getElementById('canvas'),
      autoStart: true,
      resizeTo: window,
    });

    let live2DModel;
    let isPanning = false;
    let panStartPosition = { x: 0, y: 0 };
    let stageStartPosition = { x: 0, y: 0 };
    let currentScale = 0.3;

    // Make stage interactive to ensure event propagation
    app.stage.interactive = true;
    app.stage.interactiveChildren = true;
    app.stage.hitArea = app.screen; // Set hit area to cover the screen

    // Helper function to update model scale and center position
    const updateModelTransform = () => {
      if (live2DModel) {
        live2DModel.anchor.set(0.5, 0.3);
        live2DModel.position.set(window.innerWidth / 2, window.innerHeight / 2);
        live2DModel.scale.set(currentScale, currentScale);
      }
    };

    const reloadModel = () => {
      if (live2DModel) {
        app.stage.removeChild(live2DModel);
        live2DModel.destroy(); // Properly destroy the old model
        loadModel(); // Load a new instance of the model
      }
    };

    // Load and set up the Live2D model
    const loadModel = () => {
      Live2DModel.from('/March 7th/march 7th.model3.json').then((model) => {
        live2DModel = model;
        live2DModel.interactive = true; // Ensure model is interactive
        live2DModel.buttonMode = true; // Change cursor on hover (optional)
        live2DModel.autoUpdate = true;
        app.stage.addChild(live2DModel);
        updateModelTransform();

        const succ = model.speak(someurl);
        if(succ){
          model.internalModel.lipSync.currentAudio.addEventListener("ended", () =>{});
        }
        
        console.log('Model loaded:', live2DModel);
        // test emotion

        function sleep(ms) {
          return new Promise((resolve, reject) => {
            setTimeout(() => {
              resolve(ms);
            }, ms)
          })
        }
        
        // live2DModel.internalModel.motionManager.startRandomMotion("shy", MotionPriority.NORMAL)
        // live2DModel.internalModel.motionManager.expressionManager.update()
        // async function testemote() {
        //   // live2DModel.expression("hated");

        //   await sleep(10000)
        //   live2DModel.motion('happy', undefined, MotionPriority.FORCE);
        //   console.log('Emotion: happy');
        //   await sleep(10000)
        //   // live2DModel.internalModel.motionManager.expressionManager.update()
        //   live2DModel.motion('shy');
        //   live2DModel.internalModel.motionManager.expressionManager.resetExpression()
        //   // reloadModel();
        //   console.log('Emotion: neutral');
        // }
        // live2DModel.motion("shy")

        // Replace WebSocket with Socket.IO
        const socket = io('http://127.0.0.1:8080'); // Connect to Flask-SocketIO server

        socket.on('connect', () => {
          console.log('Connected to Socket.IO server');
        });

        socket.on('disconnect', () => {
          console.log('Disconnected from Socket.IO server');
          window.location.reload();
        });

        socket.on('model_action', (data) => {
          const command = data.action.trim();
          console.log("Message from server:", command);
          live2DModel.motion("neutral", undefined, MotionPriority.FORCE)
          console.log("Try reseting expression")
          live2DModel.expression(command);
          console.log("Expression: ", command)
          // live2DModel.internalModel.motionManager.expressionManager.destroy();
          

        });

        socket.on('error', (error) => {
          console.error("Socket.IO Error: ", error);
        });
      }).catch(error => {
        console.error('Failed to load model:', error);
      });
    }

    loadModel();
    // Scroll to zoom functionality
    const handleScrollZoom = (event) => {
      const scrollDelta = event.deltaY;
      const zoomSpeed = 0.05;

      if (scrollDelta > 0) {
        currentScale = Math.max(0.1, currentScale - zoomSpeed);
      } else {
        currentScale = Math.min(2.0, currentScale + zoomSpeed);
      }

      updateModelTransform();
    };

    // Pan the entire view (stage) functionality
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

    // Add wheel event listener for zooming
    window.addEventListener('wheel', handleScrollZoom);

    // Add mouse event listeners for panning
    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    // Click test
    window.addEventListener('click', (e) => {
      console.log('Global click registered:', e.clientX, e.clientY);
    });

    // Cleanup on component unmount
    return () => {
      window.removeEventListener('wheel', handleScrollZoom);
      window.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      if (app) app.destroy(true, { children: true, texture: true, baseTexture: true });
    };
  }, []);

  return <canvas id="canvas" />;
}

export default App;