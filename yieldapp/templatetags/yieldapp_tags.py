from django import template
from ..models import Issue

register = template.Library()

# Nama file template yang akan di-render tetap sama
@register.inclusion_tag('yieldapp/partials/_issue_table.html')
def render_issue_table(): # <-- HAPUS argumen dari sini
    """
    Template tag ini sekarang mengambil SEMUA isu,
    tanpa bergantung pada filter apa pun.
    """
    # Query diubah menjadi .all() untuk mengambil semua data
    issues = Issue.objects.all().select_related('batch').order_by('is_resolved', '-updated_at')
    
    return {'issues': issues}