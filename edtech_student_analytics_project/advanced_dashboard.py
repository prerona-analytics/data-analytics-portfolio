"""
EdTech Student Analytics: Advanced Dashboard Generation
Creates 8 advanced interactive visualizations using Plotly
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set seed for reproducibility
np.random.seed(42)

print("="*70)
print("EDTECH STUDENT ANALYTICS: ADVANCED DASHBOARD GENERATION")
print("="*70)

# Generate synthetic data
print("\nGenerating synthetic student data...")
n_students = 5000
n_courses = 50

students = pd.DataFrame({
    'student_id': range(1, n_students + 1),
    'enrollment_date': pd.date_range('2025-01-01', periods=n_students, freq='H'),
    'age': np.random.normal(32, 10, n_students).astype(int),
    'enrollment_tier': np.random.choice(['Free', 'Basic', 'Premium'], n_students, p=[0.4, 0.35, 0.25]),
    'device_type': np.random.choice(['Desktop', 'Mobile', 'Tablet'], n_students, p=[0.5, 0.35, 0.15])
})

# Generate engagement and performance data
student_metrics = pd.DataFrame({
    'student_id': students['student_id'],
    'video_completion': np.random.beta(5, 2, n_students) * 100,
    'quiz_score': np.random.normal(75, 15, n_students),
    'assignment_score': np.random.normal(78, 12, n_students),
    'forum_posts': np.random.poisson(3, n_students),
    'engagement_score': np.random.uniform(20, 95, n_students),
    'course_completion': np.random.binomial(1, 0.65, n_students),
    'time_spent_hours': np.random.gamma(2, 20, n_students)
})

# Ensure scores are in valid range
student_metrics['quiz_score'] = student_metrics['quiz_score'].clip(0, 100)
student_metrics['assignment_score'] = student_metrics['assignment_score'].clip(0, 100)

df = students.merge(student_metrics, on='student_id')

print("✓ Generated {students} student records with engagement metrics".format(students=len(df)))

# --- ADVANCED VISUALIZATION 1: ENGAGEMENT DISTRIBUTION BY COHORT ---
fig1 = go.Figure()

for tier in df['enrollment_tier'].unique():
    data = df[df['enrollment_tier'] == tier]['engagement_score']
    fig1.add_trace(go.Violin(
        y=data,
        name=tier,
        side='negative',
        points='outliers',
        meanline_visible=True,
        showlegend=True
    ))

fig1.update_layout(
    title='<b>Advanced Viz 1: Engagement Score Distribution by Enrollment Tier</b><br><sub>Violin plot with outliers | Comprehensive tier comparison</sub>',
    yaxis_title='Engagement Score (0-100)',
    height=600,
    template='plotly_white',
    hovermode='closest'
)
fig1.write_html('viz_01_engagement_distribution.html')
print("✓ Saved: viz_01_engagement_distribution.html")

# --- ADVANCED VISUALIZATION 2: PERFORMANCE vs ENGAGEMENT BUBBLE CHART ---
agg_data = df.groupby('enrollment_tier').agg({
    'quiz_score': 'mean',
    'engagement_score': 'mean',
    'student_id': 'count',
    'time_spent_hours': 'mean'
}).reset_index()
agg_data.columns = ['tier', 'quiz_score', 'engagement_score', 'students', 'avg_hours']

fig2 = px.scatter(agg_data,
    x='engagement_score', y='quiz_score',
    size='students', color='tier',
    hover_data={'tier': False, 'avg_hours': ':.1f'},
    title='<b>Advanced Viz 2: Engagement vs Quiz Performance</b><br><sub>Bubble size represents student count | Color by enrollment tier</sub>',
    labels={'engagement_score': 'Engagement Score', 'quiz_score': 'Avg Quiz Score'},
    height=600
)
fig2.update_traces(marker=dict(opacity=0.7, line=dict(width=2, color='white')))
fig2.write_html('viz_02_performance_bubble.html')
print("✓ Saved: viz_02_performance_bubble.html")

# --- ADVANCED VISUALIZATION 3: HEATMAP - ENGAGEMENT vs COMPLETION ---
df['completion_status'] = df['course_completion'].map({1: 'Completed', 0: 'Dropped'})
df['engagement_bucket'] = pd.cut(df['engagement_score'], bins=[0, 33, 66, 100], labels=['Low', 'Medium', 'High'])

heatmap_data = pd.crosstab(df['engagement_bucket'], df['completion_status'], normalize='index') * 100

fig3 = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='RdYlGn',
    text=np.round(heatmap_data.values, 1),
    texttemplate='%{text}%',
    textfont={"size": 14},
    colorbar=dict(title='Percentage (%)')
))
fig3.update_layout(
    title='<b>Advanced Viz 3: Engagement Level vs Course Completion Rate Heatmap</b><br><sub>Shows completion probability by engagement tier</sub>',
    xaxis_title='Course Completion Status',
    yaxis_title='Engagement Level',
    height=500,
    template='plotly_white'
)
fig3.write_html('viz_03_completion_heatmap.html')
print("✓ Saved: viz_03_completion_heatmap.html")

# --- ADVANCED VISUALIZATION 4: PERFORMANCE TRAJECTORY ---
df_sorted = df.sort_values('quiz_score').reset_index(drop=True)
df_sorted['percentile'] = np.arange(len(df_sorted)) / len(df_sorted) * 100

fig4 = go.Figure()

for tier in df['enrollment_tier'].unique():
    tier_data = df[df['enrollment_tier'] == tier].sort_values('engagement_score').reset_index(drop=True)
    tier_data['cumulative_avg'] = tier_data['quiz_score'].rolling(100, min_periods=1).mean()
    
    fig4.add_trace(go.Scatter(
        x=tier_data['engagement_score'],
        y=tier_data['cumulative_avg'],
        mode='lines',
        name=tier,
        line=dict(width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Engagement: %{x:.1f}<br>Avg Score: %{y:.1f}<extra></extra>'
    ))

fig4.update_layout(
    title='<b>Advanced Viz 4: Performance Trajectory by Engagement Level</b><br><sub>Rolling average quiz score | Trend by enrollment tier</sub>',
    xaxis_title='Engagement Score',
    yaxis_title='Rolling Avg Quiz Score',
    height=600,
    template='plotly_white',
    hovermode='x unified'
)
fig4.write_html('viz_04_performance_trajectory.html')
print("✓ Saved: viz_04_performance_trajectory.html")

# --- ADVANCED VISUALIZATION 5: CORRELATION MATRIX HEATMAP ---
correlation_cols = ['video_completion', 'quiz_score', 'assignment_score', 'forum_posts', 'engagement_score', 'time_spent_hours']
corr_matrix = df[correlation_cols].corr()

fig5 = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=np.round(corr_matrix.values, 2),
    texttemplate='%{text}',
    textfont={"size": 11},
    colorbar=dict(title='Correlation')
))
fig5.update_layout(
    title='<b>Advanced Viz 5: Feature Correlation Matrix Heatmap</b><br><sub>Pearson correlations between engagement, performance and activity metrics</sub>',
    height=600,
    width=700,
    template='plotly_white'
)
fig5.write_html('viz_05_correlation_heatmap.html')
print("✓ Saved: viz_05_correlation_heatmap.html")

# --- ADVANCED VISUALIZATION 6: SUNBURST - ENGAGEMENT SEGMENTATION ---
df['risk_level'] = pd.cut(df['engagement_score'], bins=[0, 33, 66, 100], labels=['At Risk', 'Moderate', 'High'])
df['performance_tier'] = pd.cut(df['quiz_score'], bins=[0, 50, 75, 100], labels=['Struggling', 'Average', 'Excellent'])

sunburst_data = df.groupby(['enrollment_tier', 'risk_level', 'performance_tier']).size().reset_index(name='count')

fig6 = px.sunburst(
    sunburst_data,
    labels=sunburst_data.columns,
    parents=['', 'enrollment_tier', 'enrollment_tier'],
    values='count',
    ids=['', 'enrollment_tier', 'risk_level'],
    color='count',
    color_continuous_scale='Viridis',
    title='<b>Advanced Viz 6: Student Segmentation Sunburst</b><br><sub>Drill-down: Tier > Risk Level > Performance Tier</sub>',
    height=700
)
fig6.write_html('viz_06_segmentation_sunburst.html')
print("✓ Saved: viz_06_segmentation_sunburst.html")

# --- ADVANCED VISUALIZATION 7: BOX PLOT WITH STRIP OVERLAY ---
fig7 = go.Figure()

for tier in sorted(df['enrollment_tier'].unique()):
    tier_data = df[df['enrollment_tier'] == tier]
    
    fig7.add_trace(go.Box(
        y=tier_data['quiz_score'],
        name=tier,
        boxmean='sd',
        marker=dict(opacity=0.6)
    ))
    
    fig7.add_trace(go.Scatter(
        y=tier_data['quiz_score'],
        x=[tier] * len(tier_data),
        mode='markers',
        marker=dict(size=4, opacity=0.3, color='grey'),
        showlegend=False,
        hovertemplate='Score: %{y:.1f}<extra></extra>'
    ))

fig7.update_layout(
    title='<b>Advanced Viz 7: Quiz Score Distribution with Individual Points</b><br><sub>Box plot + strip plot | Shows mean ± SD and outliers</sub>',
    yaxis_title='Quiz Score',
    xaxis_title='Enrollment Tier',
    height=600,
    template='plotly_white',
    hovermode='closest'
)
fig7.write_html('viz_07_score_distribution.html')
print("✓ Saved: viz_07_score_distribution.html")

# --- ADVANCED VISUALIZATION 8: 3D SCATTER PLOT ---
fig8 = px.scatter_3d(
    df,
    x='engagement_score',
    y='video_completion',
    z='quiz_score',
    color='time_spent_hours',
    size='forum_posts',
    hover_name='student_id',
    color_continuous_scale='Viridis',
    title='<b>Advanced Viz 8: 3D Engagement Analysis</b><br><sub>X: Engagement | Y: Video Completion | Z: Quiz Score | Color: Time Spent | Size: Forum Posts</sub>',
    labels={
        'engagement_score': 'Engagement',
        'video_completion': 'Video Completion %',
        'quiz_score': 'Quiz Score',
        'time_spent_hours': 'Hours Spent'
    },
    height=700
)
fig8.update_traces(marker=dict(size=5, opacity=0.7))
fig8.write_html('viz_08_3d_scatter.html')
print("✓ Saved: viz_08_3d_scatter.html")

# --- COMPREHENSIVE DASHBOARD ---
print("\nGenerating comprehensive multi-chart dashboard...")

fig_dash = make_subplots(
    rows=3, cols=2,
    subplot_titles=('Engagement by Tier', 'Performance vs Engagement', 'Completion Rate', 'Time Spent Distribution', 'Forum Activity', 'Score Comparison'),
    specs=[[{'type': 'bar'}, {'type': 'scatter'}], [{'type': 'pie'}, {'type': 'box'}], [{'type': 'scatter'}, {'type': 'bar'}]]
)

# 1. Engagement by tier (bar)
engagement_by_tier = df.groupby('enrollment_tier')['engagement_score'].mean()
fig_dash.add_trace(go.Bar(x=engagement_by_tier.index, y=engagement_by_tier.values, name='Engagement', marker_color='lightblue'), row=1, col=1)

# 2. Performance vs Engagement (scatter)
fig_dash.add_trace(go.Scatter(x=df['engagement_score'], y=df['quiz_score'], mode='markers', name='Students', marker=dict(size=5, opacity=0.5, color='purple')), row=1, col=2)

# 3. Completion rate (pie)
completion_counts = df['completion_status'].value_counts()
fig_dash.add_trace(go.Pie(labels=completion_counts.index, values=completion_counts.values, name='Status'), row=2, col=1)

# 4. Time spent distribution (box)
for tier in df['enrollment_tier'].unique():
    fig_dash.add_trace(go.Box(y=df[df['enrollment_tier']==tier]['time_spent_hours'], name=tier), row=2, col=2)

# 5. Forum activity (scatter)
fig_dash.add_trace(go.Scatter(x=df['forum_posts'], y=df['quiz_score'], mode='markers', name='Forum vs Score', marker=dict(size=6, opacity=0.5, color='green')), row=3, col=1)

# 6. Score comparison (bar)
score_comparison = pd.DataFrame({
    'Quiz Avg': [df['quiz_score'].mean()],
    'Assignment Avg': [df['assignment_score'].mean()]
})
fig_dash.add_trace(go.Bar(x=score_comparison.columns, y=score_comparison.values[0], name='Score'), row=3, col=2)

fig_dash.update_xaxes(title_text='Tier', row=1, col=1)
fig_dash.update_xaxes(title_text='Engagement', row=1, col=2)
fig_dash.update_xaxes(title_text='Forum Posts', row=3, col=1)
fig_dash.update_yaxes(title_text='Engagement', row=1, col=1)
fig_dash.update_yaxes(title_text='Quiz Score', row=1, col=2)
fig_dash.update_yaxes(title_text='Quiz Score', row=3, col=1)

fig_dash.update_layout(height=1000, title_text='<b>EdTech Analytics: Comprehensive Student Dashboard</b>', showlegend=True, template='plotly_white')
fig_dash.write_html('complete_analytics_dashboard.html')
print("✓ Saved: complete_analytics_dashboard.html")

# Summary statistics
print("\n" + "="*70)
print("ANALYSIS SUMMARY")
print("="*70)
print(f"\nTotal Students Analyzed: {len(df):,}")
print(f"Average Engagement Score: {df['engagement_score'].mean():.1f}/100")
print(f"Average Quiz Score: {df['quiz_score'].mean():.1f}/100")
print(f"Course Completion Rate: {df['course_completion'].mean():.1%}")
print(f"Average Time Spent: {df['time_spent_hours'].mean():.1f} hours")
print(f"Average Forum Posts: {df['forum_posts'].mean():.1f}")
print(f"\nCompletion by Tier:")
for tier in df['enrollment_tier'].unique():
    comp_rate = df[df['enrollment_tier']==tier]['course_completion'].mean()
    print(f"  {tier}: {comp_rate:.1%}")

print("\n" + "="*70)
print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
print("="*70)
print("\nOutput files created:")
print("  • viz_01_engagement_distribution.html - Violin plots by tier")
print("  • viz_02_performance_bubble.html - Bubble chart analysis")
print("  • viz_03_completion_heatmap.html - Engagement vs completion")
print("  • viz_04_performance_trajectory.html - Trend analysis")
print("  • viz_05_correlation_heatmap.html - Feature correlations")
print("  • viz_06_segmentation_sunburst.html - Student segmentation")
print("  • viz_07_score_distribution.html - Distribution with points")
print("  • viz_08_3d_scatter.html - 3D multi-dimensional view")
print("  • complete_analytics_dashboard.html - 6-chart dashboard")
print("\nAll files are interactive - open in web browser to explore!")
