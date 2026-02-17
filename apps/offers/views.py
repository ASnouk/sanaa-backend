from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from apps.jobs.models import Job
from apps.offers.models import Offer
from apps.offers.serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):

    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Offer.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):

        offer = self.get_object()
        job = offer.job

        if job.owner != request.user:
            return Response({"error": "Not allowed"}, status=403)

        if job.status != 'open':
            return Response({"error": "Job not open"}, status=400)

        with transaction.atomic():

            offer.status = 'accepted'
            offer.save()

            Offer.objects.filter(job=job).exclude(id=offer.id).update(status='rejected')

            job.status = 'in_progress'
            job.save()

        return Response({"message": "Offer accepted"})
