# %%
# Create bar plot
fig = px.bar(df_counts, 
             x = 'ANA_classific_attuale', 
             y = 'Count', 
             color = 'tipo_sostanza',
             facet_col="Matrice", 
             barmode = "stack",
             #text_auto = True,
             color_discrete_map = colors_sostanze)

# Add text labels manually and position them on top of the bars
#fig.update_traces(texttemplate='%{y}', textposition='inside',
#                  textangle = 0, textfont_size =10,
#                  textfont_color = 'white')

fig.update_layout(
    xaxis_title="Stato Attuale",
    yaxis_title="Numero di siti",
    xaxis_title_font=dict(size=14, family='Arial', weight='bold'),
    yaxis_title_font=dict(size=14, family='Arial', weight='bold'),
    title_font = dict(size=16, family='Arial', weight='bold')
)
# fig.update_layout(
#     yaxis=dict(
#         tickmode='linear',  # Ensures evenly spaced ticks
#         dtick=1,            # Forces ticks to be spaced by 1 (integers only)
#         tickformat="d"      # Ensures numbers are displayed as whole numbers
#     )
# )
fig.update_layout(
    title=dict(
        text="Siti prioritari: Tipi di sostanze per matrice",
        x=0.5,       # Center the title
        y=0.95,      # Move title closer to the plot
        xanchor="center",
        yanchor="top",
        font=dict(
            family="Arial",  # Use a bold font
            size=18,  # Adjust font size
            color="black"
    )
))
# Show figure
fig.show()
#export_path = os.path.join(in_dir, 'Immagini/Nuove/sostanze_priori.png')
#fig.write_image(export_path, scale=3)  # Save the image as PNG
