from datetime import datetime

from django.db import models


class SoftDeleteManager(models.Manager):
    use_for_related_fields = True  # 옵션은 기본 매니저로 이 매니저를 정의한 모델이 있을 때 이 모델을 가리키는 모든 관계 참조에서 모델 매니저를 사용할 수 있도록 한다.

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def get_all_queryset(self):
        return super().get_queryset().all()


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(
        blank=True, null=True, default=None,
        editable=False, db_index=True
    )

    class Meta:
        abstract = True  # 상속 할수 있게

    objects = SoftDeleteManager()  # 커스텀 매니저

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):  # 삭제된 레코드를 복구한다.
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
