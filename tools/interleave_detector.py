import sys
import threading

class Watch:
    def __init__(self, classes=None):
        self.classes = classes or []
        self.detected_interleavings = 0
        self.active = False
        self._active_threads = {}
        self._frame_lines = {}

    def __enter__(self):
        self.active = True
        sys.settrace(self.trace_calls)
        threading.settrace(self.trace_calls)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active = False
        sys.settrace(None)
        threading.settrace(None)

    def trace_calls(self, frame, event, arg):
        if not self.active:
            return None
        if event == 'call':
            self_obj = frame.f_locals.get('self')
            if self_obj and type(self_obj) in self.classes:
                self._frame_lines[id(frame)] = 0
                return self.trace_lines
        return None

    def trace_lines(self, frame, event, arg):
        if not self.active:
            return None
        
        self_obj = frame.f_locals.get('self')
        if self_obj and type(self_obj) in self.classes:
            obj_id = id(self_obj)
            current_thread = threading.get_ident()
            
            if event == 'line':
                self._frame_lines[id(frame)] += 1
                
                # Ignorar la primera línea (el "with" o el "cur")
                if self._frame_lines[id(frame)] == 1:
                    return self.trace_lines

                # LA SOLUCIÓN: Si el objeto tiene un lock y está bloqueado...
                if hasattr(self_obj, 'lock') and self_obj.lock.locked():
                    # ...y este hilo no estaba ya en la lista de activos...
                    if obj_id not in self._active_threads or current_thread not in self._active_threads[obj_id]:
                        # ...ignoramos este hilo. Está esperando.
                        return self.trace_lines

                if obj_id not in self._active_threads:
                    self._active_threads[obj_id] = set()
                self._active_threads[obj_id].add(current_thread)
                
                # Si hay más de un hilo activo, es un interleaving
                if len(self._active_threads[obj_id]) > 1:
                    self.detected_interleavings += 1
                    
            elif event == 'return':
                if obj_id in self._active_threads:
                    self._active_threads[obj_id].discard(current_thread)
                if id(frame) in self._frame_lines:
                    del self._frame_lines[id(frame)]
                    
        return self.trace_lines

def watch(classes=None):
    return Watch(classes)
