# Инициализация класса для клинопироксенов, который содержит информацию о породах и заготовку под бинарный график:
class MinLocation:
    '''
    Класс, который позволяет задавать различные группы или сегменты минералов,
    присваивать им различные символы и цвета, а также сразу строить графику
    
    '''
    
    def __init__(self, location, name, marker, color, query, plotly_marker):
        self.location = location
        self.name = name
        self.marker = marker
        self.color = color
        self.query = query
        self.plotly_marker = plotly_marker
        self.df = df
        
    # Построение бинарных графиков:        
    def binar_plot(self, color=None, marker=None, edgecolor='black', linewidths=0.3, 
                   s=s, alpha=0.8, data=df, name=None):
        actual_color = color if color is not None else self.color
        actual_marker = marker if marker is not None else self.marker
        actual_name = name if name is not None else self.name
        axs[i].scatter(x=x, y=y, data=data.query(self.query),
                edgecolor=edgecolor, linewidths=linewidths, s=s, alpha=alpha, 
                marker=actual_marker, c=actual_color, label=actual_name)
        
    def reg_plot(self, color=None, edgecolor='black', linewidths=0.3, s=s, alpha=0.6, data=df, 
                 logistic=False, order=1, ci=95, scatter=False):
        actual_color = color if color is not None else self.color
        sns.regplot(data=data.query(self.query), x=x, y=y, ci=ci, marker=self.marker, color=str(alpha), scatter=scatter,
            line_kws=dict(color=actual_color), order=order, logistic=logistic, ax=axs[i])
    
    def kde_plot(self, color=None, edgecolor='black', linewidths=2.0, s=s, alpha=1, data=df, bw_adjust=1,
                 logistic=False, levels=1, ci=95, thresh=.1, scatter=False):
        actual_color = color if color is not None else self.color       
        sns.kdeplot(data=data.query(self.query), x=x, y=y, linestyle='dotted', bw_adjust=bw_adjust, 
                    color=actual_color, levels=levels, thresh=thresh, ax=axs[i], linestyles='--', linewidths=linewidths)   
        
    # Построение треугольных диаграмм:    
    def tern_plot(self, edgecolor='black', color=None, linewidths=0.3, s=s, alpha=0.6, data=df):
        actual_color = color if color is not None else self.color       
        data_for_plot = data=data.query(self.query)
        t, l, r = data_for_plot[t_element], data_for_plot[l_element], data_for_plot[r_element]   
        ax.scatter(t, l, r, s=s, edgecolors=edgecolor, linewidths=linewidths, alpha=alpha, 
                marker=self.marker, c=actual_color, label=self.name)
        
    # Построение гистограмм:      
    def hist_plot(self, edgecolor='black', color=None, linewidths=0.3, bins=None,
                  alpha=0.6, data=df, axis=None, binwidth=0.5):
        actual_color = color if color is not None else self.color       
        sns.histplot(x=y, data=data.query(self.query), binwidth=binwidth, ax=axs[axis],
                edgecolor=edgecolor, linewidths=linewidths, alpha=alpha, bins=bins,
                color=actual_color, label=self.name)
    
    # Построение бинарных графиков Plotly: 
    def plotly_scatter(self, edgecolor='black', linewidths=0.3, alpha=0.6, df=df, x='MgO', y='TiO2', s=s, legendgroup=None):
        plot = go.Scatter(x=df.query(self.query)[x], y=df.query(self.query)[y], mode='markers', name=self.name,
                   marker_symbol=self.plotly_marker, marker_line_color=edgecolor, marker_color=self.color,
                   marker_line_width=linewidths, marker_size=s/5, marker_opacity=alpha, legendgroup=legendgroup)
        return plot
        
    # Построение треугольных диаграмм Plotly:       
    def plotly_tern(self, edgecolor='black', linewidths=0.3, alpha=0.6, df=df, a='MgO', b='TiO2', c='TiO2', s=s, legendgroup=None):
        plot =  go.Scatterternary(a=df.query(self.query)[a], b=df.query(self.query)[b], c=df.query(self.query)[c],   
                      mode='markers', name=self.name, marker_line_color=edgecolor, marker_line_width=linewidths,
                      marker={'symbol': self.plotly_marker, 'color': self.color, 'size': s/5},
                      marker_opacity=alpha, legendgroup=legendgroup)
        return plot