from rest_framework.exceptions import Throttled


class ThrottleMessageMixin:
    """
    Surface each throttle's custom ``message`` in the 429 response body.

    DRF's default ``check_throttles`` raises ``Throttled`` with only the wait
    time and never reads the ``message`` attribute defined on a throttle class,
    so custom throttle messages are silently dropped. This mixin overrides that
    hook to capture the message from the throttle that rejected the request and
    pass it through as the response ``detail``. The wait duration is preserved
    because DRF also uses it to populate the ``Retry-After`` response header.
    """

    def check_throttles(self, request):
        throttle_durations = []
        throttle_message = None

        for throttle in self.get_throttles():
            if not throttle.allow_request(request, self):
                throttle_durations.append(throttle.wait())
                # The first rejecting throttle owns the message. Each view here
                # attaches a single scope-specific throttle, so there is no
                # ambiguity about which message to surface.
                if throttle_message is None:
                    throttle_message = getattr(throttle, "message", None)

        if throttle_durations:
            # A throttle can return None from wait(); drop those before taking
            # the longest remaining cooldown as the reported retry window.
            durations = [d for d in throttle_durations if d is not None]
            duration = max(durations, default=None)
            raise Throttled(wait=duration, detail=throttle_message)
