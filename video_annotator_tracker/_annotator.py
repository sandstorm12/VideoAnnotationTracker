import cv2


class AnnotatorTracker(object):
    FRAME_NAME = "VideoAnnotatorTracker"

    def __init__(self, path, width=1280, height=720, miss_forget_count=10):
        self.cap = cv2.VideoCapture(path)
        self.trackers = {}
        self.miss_counter = {}
        self.next_id = 0
        self.miss_forget_count = miss_forget_count
        self.width = width
        self.height = height

        self.bbs = []
        self.temp_coordinates = None
        
        self._read_next_frame()

        cv2.namedWindow(self.FRAME_NAME)
        cv2.setMouseCallback(
            self.FRAME_NAME, self._on_mouse_event
        )

    def _on_mouse_event(self, event, x, y, flags, parameters):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.temp_coordinates = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            x1, y1 = self.temp_coordinates 
            width = x - x1
            height = y - y1
            self.bbs.append((x1, y1, width, height))

            for coordinates in self.bbs:
                cv2.rectangle(
                    self.frame_buffer,
                    (coordinates[0], coordinates[1]),
                    (
                        coordinates[0] + coordinates[2],
                        coordinates[1] + coordinates[3]
                    ),
                    (36,255,12), 2
                )
                cv2.imshow(self.FRAME_NAME, self.frame_buffer)

    def _add_new_objects(self):
        while len(self.bbs) > 0:
            self.trackers[self.next_id] = cv2.TrackerKCF_create()
            self.miss_counter[self.next_id] = 0
            ok = self.trackers[self.next_id].init(
                self.frame_buffer, self.bbs[0]
            )

            self.next_id += 1

            del self.bbs[0]

    def _read_next_frame(self):
        ret, self.frame_buffer = self.cap.read()
        self.frame_buffer = cv2.resize(
            self.frame_buffer, (self.width, self.height)
        )

        return ret

    def _update_tracker(self):
        for track_id in list(self.trackers.keys()):
            ok, bbox = self.trackers[track_id].update(self.frame_buffer)
            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(self.frame_buffer, p1, p2, (255,0,0), 2, 1)
                cv2.putText(
                    self.frame_buffer, str(track_id), (p1[0], p2[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
                )
            else:
                self.miss_counter[track_id] += 1
                if self.miss_counter[track_id] > self.miss_forget_count:
                    del self.trackers[track_id]
                    del self.miss_counter[track_id]

    def _next_frame(self):
        self._add_new_objects()

        ret = self._read_next_frame()

        self._update_tracker()

        return ret, self.frame_buffer

    def run(self):
        while True:
            ret, next_frame = self._next_frame()
            if ret:
                cv2.imshow(
                    self.FRAME_NAME, next_frame
                )
                key = cv2.waitKey()
                if key == ord('q'):
                    break
            else:
                break


# Just for test
if __name__ == "__main__":
    annotator_tracker = AnnotatorTracker(path="sample.mp4")
    annotator_tracker.run()
