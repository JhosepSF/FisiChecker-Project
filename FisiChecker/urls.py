# FisiChecker/urls.py
from django.contrib import admin
from django.urls import path
from audits.views import (
    # Vistas de Plantillas HTML
    panel_page_view,
    login_page_view,
    logout_page_view,
    audit_detail_page_view,
    colab_analysis_page_view,
    
    # API Views
    AuditView, 
    AuditRetrieveView, 
    AuditListView,
    StatisticsGlobalView,
    StatisticsVerdictDistributionView,
    StatisticsCriteriaView,
    StatisticsLevelView,
    StatisticsPrincipleView,
    StatisticsTimelineView,
    StatisticsURLRankingView,
    StatisticsSourceComparisonView,
    StatisticsAuditDetailView,
    StatisticsComprehensiveReportView,
    StatisticsAccessibilityLevelsView,
    StatisticsAccessibilityByWCAGView,
    
    # Autenticación API
    login_view,
    logout_view,
    current_user_view,
    
    # Exportación
    export_csv_view,
    export_excel_view,
    delete_audit_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ===============================
    # Vistas Frontend (HTML Templates)
    # ===============================
    path('', panel_page_view, name='panel'),
    path('panel/', panel_page_view, name='panel_page'),
    path('login/', login_page_view, name='login_page'),
    path('logout/', logout_page_view, name='logout_view'),
    path('audits/<int:audit_id>/', audit_detail_page_view, name='audit_detail_page'),
    path('audit/<int:audit_id>/', audit_detail_page_view, name='audit_detail_alias'),
    path('colab/', colab_analysis_page_view, name='colab_analysis'),
    
    # ===============================
    # API REST Endpoints
    # ===============================
    # Autenticación
    path('api/auth/login', login_view, name='api-login'),
    path('api/auth/logout', logout_view, name='api-logout'),
    path('api/auth/user', current_user_view, name='current-user'),
    
    # Auditorías
    path('api/audit', AuditView.as_view(), name='api-audit-create'),
    path('api/audits/<int:pk>', AuditRetrieveView.as_view(), name='api-audit-detail'),
    path('api/audits', AuditListView.as_view(), name='api-audit-list'),
    
    # Estadísticas
    path('api/statistics/global/', StatisticsGlobalView.as_view(), name='statistics-global'),
    path('api/statistics/verdicts/', StatisticsVerdictDistributionView.as_view(), name='statistics-verdicts'),
    path('api/statistics/criteria/', StatisticsCriteriaView.as_view(), name='statistics-criteria'),
    path('api/statistics/levels/', StatisticsLevelView.as_view(), name='statistics-levels'),
    path('api/statistics/principles/', StatisticsPrincipleView.as_view(), name='statistics-principles'),
    path('api/statistics/timeline/', StatisticsTimelineView.as_view(), name='statistics-timeline'),
    path('api/statistics/ranking/', StatisticsURLRankingView.as_view(), name='statistics-ranking'),
    path('api/statistics/sources/', StatisticsSourceComparisonView.as_view(), name='statistics-sources'),
    path('api/statistics/audit/<int:audit_id>/', StatisticsAuditDetailView.as_view(), name='statistics-audit-detail'),
    path('api/statistics/report/', StatisticsComprehensiveReportView.as_view(), name='statistics-report'),
    
    # Estadísticas Hilera (Niveles de Accesibilidad)
    path('api/statistics/accessibility-levels/', StatisticsAccessibilityLevelsView.as_view(), name='statistics-accessibility-levels'),
    path('api/statistics/accessibility-by-wcag/', StatisticsAccessibilityByWCAGView.as_view(), name='statistics-accessibility-wcag'),
    
    # Exportación
    path('api/export/csv', export_csv_view, name='export-csv'),
    path('api/export/excel', export_excel_view, name='export-excel'),
    
    # Borrar auditoría
    path('api/audits/<int:audit_id>/delete/', delete_audit_view, name='delete-audit'),
]


