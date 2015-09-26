package utakvideo.isisredirect.co.jp.utakvideo;

import android.media.MediaPlayer;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = MainActivity.class.getSimpleName();

    private boolean playing = false;
    private boolean videoplaying = false;
    private FullScreenVideoView videoView;

    private Handler handler = new Handler();
    private Timer prepareTimer = null;

    private void addVideoCallbacks() {
        Log.d(TAG, "addVideoCallbacks");
        videoView.setOnPreparedListener(videoPreparedListener);
        videoView.setOnCompletionListener(videoCompletionListener);
        videoView.setOnErrorListener(videoErrorListener);
    }

    private void removeVideoCallbacks() {
        Log.d(TAG, "removeVideoCallbacks");
        videoView.setOnPreparedListener(null);
        videoView.setOnCompletionListener(null);
        videoView.setOnErrorListener(null);
    }

    private MediaPlayer.OnPreparedListener videoPreparedListener = new MediaPlayer.OnPreparedListener() {
        @Override
        public void onPrepared(MediaPlayer mp) {
            Log.d(TAG, "onPrepared");
            videoView.setVideoWidth(mp.getVideoWidth());
            videoView.setVideoHeight(mp.getVideoHeight());
            videoView.invalidate();
            //duration = mp.getDuration();
            final MediaPlayer fmp = mp;

            fmp.start();
            if (prepareTimer != null) {
                prepareTimer.cancel();
                prepareTimer = null;
            }
            prepareTimer = new Timer();
            TimerTask task = new TimerTask() {
                @Override
                public void run() {
                    handler.post(new Runnable() {
                        @Override
                        public void run() {
                            if (!playing) {
                                fmp.pause();
                                fmp.seekTo(0);
                            }
                        }
                    });
                }
            };
            prepareTimer.schedule(task, 500);
        }
    };
    private MediaPlayer.OnCompletionListener videoCompletionListener = new MediaPlayer.OnCompletionListener() {
        @Override
        public void onCompletion(MediaPlayer mp) {
            Log.d(TAG, "onCompletion");
            //duration = 0;
            stopvideo();
        }
    };

    private MediaPlayer.OnErrorListener videoErrorListener = new MediaPlayer.OnErrorListener(){
        @Override
        public boolean onError(MediaPlayer mp, int what, int extra) {
            Log.d(TAG, "Video error " + what + " " + extra );
            //duration = 0;
            stopvideo();
            return true;    // no error dialog
        }
    };

    /**
     *
     * @param path
     *  "file:///android_asset"+filename
     */
    public void playvideo(String path) {
        if (path != null) {
            videoplaying = true;
            Log.d(TAG, "playvideo " + path);
            if (playing) {
             }
            addVideoCallbacks();
            videoView.setVideoPath(path);
        }
    }

    public void pausevideo() {
        if (videoView.isPlaying()) {
            videoView.pause();
        }
    }

    public void stopvideo() {
        boolean saved = videoplaying;
        juststopvideo();
        if (playing) {
        }
    }
    private void juststopvideo() {
        if (prepareTimer != null) {
            prepareTimer.cancel();
            prepareTimer = null;
        }
        removeVideoCallbacks();
        videoView.stopPlayback();
        videoView.setVisibility(View.INVISIBLE);
        Log.d(TAG, "juststopvideo " + (videoView.getVisibility() == View.VISIBLE));
//        videoplaying = false;
    }

    private void resumePlayingContext() {
        if (videoplaying) {
            addVideoCallbacks();
            videoView.resume();
        }
        playing = true;
    }

    private void pausePlayingContext() {
        if (videoplaying) {
            removeVideoCallbacks();
            videoView.suspend();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        videoView = (FullScreenVideoView) findViewById(R.id.video);
        videoplaying = false;
    }

    private void pushPlayButton() {
        if (videoplaying) {
            if (playing) {
                if (videoView.isPlaying()) {
                    videoView.pause();
                }
            }else{
                if (!videoView.isPlaying()) {
                    videoView.start();
                }
            }
        }else{
        }
        playing = !playing;
    }

}
