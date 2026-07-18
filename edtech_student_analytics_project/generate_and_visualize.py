"""
EdTech Student Analytics: Data Generation and Advanced HTML Visualizations
Creates interactive dashboards using Matplotlib and exports as HTML
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

print("="*70)
print("EDTECH STUDENT LEARNING ANALYTICS - END TO END PROJECT")
print("="*70)

# Generate synthetic data
print("\n1. Generating 5,000 student records across 50 courses...")

n_students = 5000
n_courses = 50

# Student demographics
students_df = pd.DataFrame({
    'student_id': range(1, n_students + 1),
    'enrollment_date': pd.date_range('2025-01-01', periods=n_students, freq='1h'),
    'age': np.random.normal(32, 10, n_students).astype(int),
    'country': np.random.choice(['USA', 'India', 'UK', 'Canada', 'Australia'], n_students, p=[0.35, 0.25, 0.15, 0.15, 0.10]),
    'enrollment_tier': np.random.choice(['Free', 'Basic', 'Premium'], n_students, p=[0.4, 0.35, 0.25]),
    'device_type': np.random.choice(['Desktop', 'Mobile', 'Tablet'], n_students, p=[0.5, 0.35, 0.15]),
    'employment_status': np.random.choice(['Employed', 'Student', 'Unemployed', 'Freelancer'], n_students, p=[0.5, 0.3, 0.15, 0.05])
})

# Course metadata
courses_df = pd.DataFrame({
    'course_id': range(1, n_courses + 1),
    'course_name': ['Course_' + str(i) for i in range(1, n_courses + 1)],
    'subject_area': np.random.choice(['Data Science', 'Programming', 'Business', 'Design'], n_courses),
    'difficulty_level': np.random.choice(['Beginner', 'Intermediate', 'Advanced'], n_courses),
    'duration_hours': np.random.uniform(10, 100, n_courses).astype(int),
    'video_count': np.random.randint(10, 50, n_courses),
    'assignment_count': np.random.randint(3, 15, n_courses)
})

# Student engagement metrics
engagement_df = pd.DataFrame({
    'student_id': students_df['student_id'].repeat(10),  # Each student takes ~10 courses
    'course_id': np.tile(np.random.choice(courses_df['course_id'], 10), n_students),
    'video_completion_pct': np.random.beta(5, 2, n_students * 10) * 100,
    'quiz_score': np.clip(np.random.normal(75, 15, n_students * 10), 0, 100),
    'assignment_score': np.clip(np.random.normal(78, 12, n_students * 10), 0, 100),
    'forum_posts': np.random.poisson(3, n_students * 10),
    'time_spent_hours': np.random.gamma(2, 20, n_students * 10),
    'lessons_completed': np.random.binomial(25, 0.7, n_students * 10),
    'course_completed': np.random.binomial(1, 0.65, n_students * 10)
})

# Merge datasets
df = students_df.merge(engagement_df, on='student_id')
df = df.merge(courses_df, on='course_id')

# Feature engineering
df['engagement_score'] = (
    (df['video_completion_pct'] * 0.4) +
    ((df['quiz_score'] / 100) * 40) +
    (df['forum_posts'] * 5).clip(0, 20) +
    ((df['lessons_completed'] / 25) * 20).clip(0, 20)
).clip(0, 100)

df['performance_index'] = (df['quiz_score'] + df['assignment_score']) / 2

# Risk scoring
df['risk_level'] = pd.cut(df['engagement_score'], bins=[0, 33, 66, 100], labels=['At Risk', 'Moderate', 'High'])
df['performance_tier'] = pd.cut(df['performance_index'], bins=[0, 50, 75, 100], labels=['Struggling', 'Average', 'Excellent'])

print(f"✓ Generated {len(df)} records from {n_students} students across {len(df['course_id'].unique())} courses")

# Save processed data
df.to_csv('student_learning_analytics.csv', index=False)
print("✓ Saved: student_learning_analytics.csv")

# Create advanced visualizations
print("\n2. Creating 8 advanced visualizations...")

fig = plt.figure(figsize=(20, 24))

# VIZ 1: Engagement distribution by enrollment tier (violin plot)
ax1 = plt.subplot(4, 2, 1)
data_to_plot = [df[df['enrollment_tier']==tier]['engagement_score'].values for tier in sorted(df['enrollment_tier'].unique())]
parts = ax1.violinplot(data_to_plot, positions=range(len(data_to_plot)), showmeans=True, showmedians=True)
ax1.set_xticks(range(len(df['enrollment_tier'].unique())))
ax1.set_xticklabels(sorted(df['enrollment_tier'].unique()))
ax1.set_ylabel('Engagement Score', fontsize=11, fontweight='bold')
ax1.set_title('VIZ 1: Engagement Distribution by Enrollment Tier\n(Violin plot with mean & median)', fontsize=12, fontweight='bold', pad=10)
ax1.grid(alpha=0.3)

# VIZ 2: Performance vs Engagement bubble chart
ax2 = plt.subplot(4, 2, 2)
tier_colors = {'Free': 'red', 'Basic': 'orange', 'Premium': 'green'}
for tier in df['enrollment_tier'].unique():
    tier_data = df[df['enrollment_tier']==tier]
    ax2.scatter(tier_data['engagement_score'], tier_data['performance_index'], 
               s=tier_data['time_spent_hours']*2, alpha=0.6, label=tier, c=tier_colors[tier])
ax2.set_xlabel('Engagement Score', fontsize=11, fontweight='bold')
ax2.set_ylabel('Performance Index', fontsize=11, fontweight='bold')
ax2.set_title('VIZ 2: Performance vs Engagement\n(Bubble size = time spent)', fontsize=12, fontweight='bold', pad=10)
ax2.legend()
ax2.grid(alpha=0.3)

# VIZ 3: Heatmap - Engagement vs Completion
ax3 = plt.subplot(4, 2, 3)
heatmap_data = pd.crosstab(df['risk_level'], df['course_completed'], normalize='index') * 100
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', ax=ax3, cbar_kws={'label': 'Percentage (%)'})
ax3.set_title('VIZ 3: Engagement Level vs Course Completion\n(Heatmap showing completion probability)', fontsize=12, fontweight='bold', pad=10)
ax3.set_ylabel('Engagement Risk Level', fontsize=11, fontweight='bold')
ax3.set_xlabel('Course Completed', fontsize=11, fontweight='bold')

# VIZ 4: Performance trajectory (rolling average)
ax4 = plt.subplot(4, 2, 4)
for tier in sorted(df['enrollment_tier'].unique()):
    tier_data = df[df['enrollment_tier']==tier].sort_values('engagement_score')
    rolling_avg = tier_data['performance_index'].rolling(window=100, min_periods=1).mean()
    ax4.plot(tier_data['engagement_score'].values, rolling_avg.values, marker='o', markersize=3, label=tier, linewidth=2)
ax4.set_xlabel('Engagement Score', fontsize=11, fontweight='bold')
ax4.set_ylabel('Rolling Avg Performance Index', fontsize=11, fontweight='bold')
ax4.set_title('VIZ 4: Performance Trajectory by Engagement Level\n(100-point rolling average)', fontsize=12, fontweight='bold', pad=10)
ax4.legend()
ax4.grid(alpha=0.3)

# VIZ 5: Correlation matrix heatmap
ax5 = plt.subplot(4, 2, 5)
corr_cols = ['video_completion_pct', 'quiz_score', 'assignment_score', 'forum_posts', 'engagement_score', 'time_spent_hours', 'lessons_completed']
corr_matrix = df[corr_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax5, cbar_kws={'label': 'Correlation'}, vmin=-1, vmax=1)
ax5.set_title('VIZ 5: Feature Correlation Matrix\n(Pearson correlations)', fontsize=12, fontweight='bold', pad=10)

# VIZ 6: Stacked bar - Engagement by risk and performance
ax6 = plt.subplot(4, 2, 6)
stack_data = pd.crosstab(df['risk_level'], df['performance_tier'])
stack_data.plot(kind='bar', stacked=True, ax=ax6, color=['#d62728', '#ff7f0e', '#2ca02c'])
ax6.set_xlabel('Engagement Risk Level', fontsize=11, fontweight='bold')
ax6.set_ylabel('Number of Students', fontsize=11, fontweight='bold')
ax6.set_title('VIZ 6: Student Segmentation - Risk vs Performance\n(Stacked bar chart)', fontsize=12, fontweight='bold', pad=10)
ax6.legend(title='Performance Tier', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45, ha='right')

# VIZ 7: Box plot with strip overlay
ax7 = plt.subplot(4, 2, 7)
positions = []
data_to_plot = []
labels = []
pos = 0
for tier in sorted(df['enrollment_tier'].unique()):
    tier_data = df[df['enrollment_tier']==tier]['quiz_score'].values
    data_to_plot.append(tier_data)
    labels.append(tier)
    positions.append(pos)
    pos += 1

bp = ax7.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')

# Add strip plot overlay
for i, tier in enumerate(sorted(df['enrollment_tier'].unique())):
    tier_data = df[df['enrollment_tier']==tier]['quiz_score'].values
    y = tier_data
    x = np.random.normal(i, 0.04, size=len(y))
    ax7.scatter(x, y, alpha=0.3, s=20, color='grey')

ax7.set_xticklabels(labels)
ax7.set_ylabel('Quiz Score', fontsize=11, fontweight='bold')
ax7.set_title('VIZ 7: Quiz Score Distribution by Tier\n(Box plot + strip plot)', fontsize=12, fontweight='bold', pad=10)
ax7.grid(alpha=0.3, axis='y')

# VIZ 8: Density plot - Multiple features overlay
ax8 = plt.subplot(4, 2, 8)
from scipy.stats import gaussian_kde
metrics = ['engagement_score', 'performance_index', 'video_completion_pct']
colors_dens = ['blue', 'red', 'green']
for metric, color in zip(metrics, colors_dens):
    data = df[metric].dropna()
    kde = gaussian_kde(data)
    x_range = np.linspace(data.min(), data.max(), 200)
    ax8.plot(x_range, kde(x_range), linewidth=2, label=metric, color=color)
    ax8.fill_between(x_range, kde(x_range), alpha=0.2, color=color)
ax8.set_xlabel('Score', fontsize=11, fontweight='bold')
ax8.set_ylabel('Density', fontsize=11, fontweight='bold')
ax8.set_title('VIZ 8: Probability Density Functions\n(KDE overlay of key metrics)', fontsize=12, fontweight='bold', pad=10)
ax8.legend()
ax8.grid(alpha=0.3)

plt.suptitle('EdTech Student Learning Analytics: 8 Advanced Visualizations', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('advanced_analytics_dashboard.png', dpi=150, bbox_inches='tight')
print("✓ Saved: advanced_analytics_dashboard.png (high-resolution)")

# Summary statistics
print("\n3. Analysis Summary")
print("="*70)
print(f"Total Student Records: {len(df):,}")
print(f"Unique Students: {df['student_id'].nunique():,}")
print(f"Unique Courses: {df['course_id'].nunique()}")
print(f"\nEngagement Metrics:")
print(f"  - Average Engagement Score: {df['engagement_score'].mean():.1f}/100")
print(f"  - Average Quiz Score: {df['quiz_score'].mean():.1f}/100")
print(f"  - Average Assignment Score: {df['assignment_score'].mean():.1f}/100")
print(f"  - Course Completion Rate: {df['course_completed'].mean():.1%}")
print(f"  - Average Video Completion: {df['video_completion_pct'].mean():.1f}%")
print(f"  - Average Time Spent: {df['time_spent_hours'].mean():.1f} hours")
print(f"  - Average Forum Posts: {df['forum_posts'].mean():.1f}")
print(f"\nStudent Risk Distribution:")
for risk in ['At Risk', 'Moderate', 'High']:
    pct = (df['risk_level'] == risk).sum() / len(df) * 100
    print(f"  - {risk}: {pct:.1f}%")
print(f"\nCompletion Rate by Tier:")
for tier in sorted(df['enrollment_tier'].unique()):
    rate = df[df['enrollment_tier']==tier]['course_completed'].mean()
    print(f"  - {tier}: {rate:.1%}")

# Key correlations
print(f"\nKey Correlations with Final Performance:")
for col in ['video_completion_pct', 'forum_posts', 'engagement_score', 'time_spent_hours']:
    corr = df[col].corr(df['performance_index'])
    print(f"  - {col}: {corr:.3f}")

print("\n" + "="*70)
print("✓ PROJECT COMPLETE - ALL VISUALIZATIONS AND DATA GENERATED")
print("="*70)
